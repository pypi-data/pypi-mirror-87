# ==================================================================
#       文 件 名: decorators.py
#       概    要: 装饰器
#       作    者: IT小强 
#       创建时间: 8/10/20 1:37 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from functools import wraps

OTP_NOT_REQUIRED_KEY: str = 'otp_not_required'


def otp_not_required(func):
    """
    不验证OTP
    :return:
    """

    setattr(func, OTP_NOT_REQUIRED_KEY, True)

    @wraps(func)
    def __otp_not_required(*args, **kw):
        return func(*args, **kw)

    return __otp_not_required


def otp_required(required: bool = True):
    """
    是否验证OTP
    :param required:
    :return:
    """

    def wrapper(func):
        setattr(func, OTP_NOT_REQUIRED_KEY, not bool(required))

        @wraps(func)
        def __otp_required(*args, **kwargs):
            return func(*args, **kwargs)

        return __otp_required

    return wrapper
