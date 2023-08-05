# ==================================================================
#       文 件 名: __init__.py
#       概    要: OTP増强
#       作    者: IT小强 
#       创建时间: 8/10/20 10:14 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.contrib.auth import user_logged_out, user_logged_in

from .device import DeviceManage


def _user_logged_in_otp(sender, request, user, **kwargs):
    DeviceManage.otp_login(request, None)


user_logged_in.connect(_user_logged_in_otp)


def _user_logged_out_otp(sender, request, user, **kwargs):
    DeviceManage.otp_logout(request, user)


user_logged_out.connect(_user_logged_out_otp)
