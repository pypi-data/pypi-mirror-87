"""
ip_cz.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-11-26 13:56
"""

import struct
from pathlib import Path

from .util import string_to_ip, ip_to_string


class IPCz:
    """
    纯真IP地址解析类
    """

    # 数据文件路径
    __database_file = Path(__file__).resolve(strict=True).parent / 'data' / 'qqwry.dat'
    __cur_start_ip = None
    __cur_end_ip_offset = None
    __cur_end_ip = None

    def __init__(self, database_file=None):
        if database_file:
            self.__database_file = database_file
        self.__f_db = open(self.__database_file, "rb")
        bs = self.__f_db.read(8)
        (self.__first_index, self.__last_index) = struct.unpack('II', bs)
        self.__index_count = int((self.__last_index - self.__first_index) / 7 + 1)

    def get_version(self):
        """
        获取版本信息，最后一条IP记录 255.255.255.0- 是版本信息
        :return: str
        """
        return self.get_ip_address('255.255.255.255')

    def __get_area_addr(self, offset=0):
        if offset:
            self.__f_db.seek(offset)
        bs = self.__f_db.read(1)
        (byte,) = struct.unpack('B', bs)
        if byte == 0x01 or byte == 0x02:
            p = self.__get_long3()
            if p:
                return self.__get_offset_string(p)
            else:
                return ""
        else:
            self.__f_db.seek(-1, 1)
            return self.__get_offset_string(offset)

    def __get_addr(self, offset):
        """
        获取offset处记录区地址信息(包含国家和地区)
        如果是中国ip，则是 "xx省xx市 xxxxx地区" 这样的形式
        (比如:"福建省 电信", "澳大利亚 墨尔本Goldenit有限公司")
        :param offset:
        :return:str
        """
        self.__f_db.seek(offset + 4)
        bs = self.__f_db.read(1)
        (byte,) = struct.unpack('B', bs)
        if byte == 0x01:  # 重定向模式1
            country_offset = self.__get_long3()
            self.__f_db.seek(country_offset)
            bs = self.__f_db.read(1)
            (b,) = struct.unpack('B', bs)
            if b == 0x02:
                country_addr = self.__get_offset_string(self.__get_long3())
                self.__f_db.seek(country_offset + 4)
            else:
                country_addr = self.__get_offset_string(country_offset)
            area_addr = self.__get_area_addr()
        elif byte == 0x02:  # 重定向模式2
            country_addr = self.__get_offset_string(self.__get_long3())
            area_addr = self.__get_area_addr(offset + 8)
        else:  # 字符串模式
            country_addr = self.__get_offset_string(offset + 4)
            area_addr = self.__get_area_addr()
        return country_addr + " " + area_addr

    def __set_ip_range(self, index):
        offset = self.__first_index + index * 7
        self.__f_db.seek(offset)
        buf = self.__f_db.read(7)
        (self.__cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
        self.__cur_end_ip_offset = of1 + (of2 << 16)
        self.__f_db.seek(self.__cur_end_ip_offset)
        buf = self.__f_db.read(4)
        (self.__cur_end_ip,) = struct.unpack("I", buf)

    def get_ip_address(self, ip: str) -> str:
        """
        通过ip查找其地址
        :param ip: (int or str)
        :return: str
        """
        if type(ip) == str:
            ip = string_to_ip(ip)
        ll = 0
        rr = self.__index_count - 1
        while ll < rr - 1:
            M = int((ll + rr) / 2)
            self.__set_ip_range(M)
            if ip == self.__cur_start_ip:
                ll = M
                break
            if ip > self.__cur_start_ip:
                ll = M
            else:
                rr = M
        self.__set_ip_range(ll)
        # version information, 255.255.255.X, urgy but useful
        if ip & 0xffffff00 == 0xffffff00:
            self.__set_ip_range(rr)
        if self.__cur_start_ip <= ip <= self.__cur_end_ip:
            address = self.__get_addr(self.__cur_end_ip_offset)
        else:
            address = "未找到该IP的地址"
        return address.replace('CZ88.NET', '')

    def get_ip_range(self, ip: str) -> str:
        """
        返回ip所在记录的IP段
        :param  ip str
        :return: str
        """
        if type(ip) == str:
            ip = string_to_ip(ip)
        self.get_ip_address(ip)
        return ip_to_string(self.__cur_start_ip) + ' - ' + ip_to_string(self.__cur_end_ip)

    def __get_offset_string(self, offset=0):
        """
        获取文件偏移处的字符串(以'\0'结尾)
        :param offset: 偏移
        :return: str
        """
        if offset:
            self.__f_db.seek(offset)
        bs = b''
        ch = self.__f_db.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            bs += ch
            ch = self.__f_db.read(1)
            (byte,) = struct.unpack('B', ch)
        return bs.decode('gbk')

    def __get_long3(self, offset=0):
        """
        3字节的数值
        :param offset:
        :return:
        """
        if offset:
            self.__f_db.seek(offset)
        bs = self.__f_db.read(3)
        (a, b) = struct.unpack('HB', bs)
        return (b << 16) + a
