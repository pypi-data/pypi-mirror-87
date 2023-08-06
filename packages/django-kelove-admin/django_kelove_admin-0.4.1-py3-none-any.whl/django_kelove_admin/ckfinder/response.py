# ==================================================================
#       文 件 名: response.py
#       概    要: Response数据整合
#       作    者: IT小强 
#       创建时间: 7/5/20 10:38 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================


class Response:
    headers = {"X-Frame-Options": "SAMEORIGIN"}

    @classmethod
    def response(
            cls,
            content,
            content_type: str = 'application/json',
            status_code: int = 200,
            headers: dict = None
    ) -> dict:
        """
        返回 response 信息
        :param content:
        :param content_type:
        :param status_code:
        :param headers:
        :return:
        """

        if headers is None:
            headers = {}
        return {
            "content_type": content_type,
            "status_code": status_code,
            'content': content,
            'headers': {**cls.headers, **headers}
        }

    @classmethod
    def acl_error(cls, content: str, status_code: int = 401, content_type: str = '', headers: dict = None):
        return cls.error(content=content, content_type=content_type, status_code=status_code, headers=headers)

    @classmethod
    def error(cls, content: str, status_code: int = 500, content_type: str = '', headers: dict = None):
        return cls.response(content=content, content_type=content_type, status_code=status_code, headers=headers)
