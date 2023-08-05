"""
util.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-11-26 14:01
"""

import socket
import struct


def ip_to_string(ip) -> str:
    """
    整数IP转化为IP字符串
    :param ip:
    :return:
    """
    return str(ip >> 24) + '.' + str((ip >> 16) & 0xff) + '.' + str((ip >> 8) & 0xff) + '.' + str(ip & 0xff)


def string_to_ip(s):
    """
    IP字符串转换为整数IP
    :param s:
    :return:
    """
    (ip,) = struct.unpack('I', socket.inet_aton(s))
    return ((ip >> 24) & 0xff) | ((ip & 0xff) << 24) | ((ip >> 8) & 0xff00) | ((ip & 0xff00) << 8)
