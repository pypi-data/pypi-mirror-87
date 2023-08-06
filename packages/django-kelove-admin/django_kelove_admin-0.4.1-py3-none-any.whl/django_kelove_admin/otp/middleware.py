# ==================================================================
#       文 件 名: middleware.py
#       概    要: 中间件
#       作    者: IT小强 
#       创建时间: 8/10/20 10:16 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlquote
from django.db import OperationalError, connections

from .decorators import OTP_NOT_REQUIRED_KEY
from .device import DeviceManage

from ..conf import settings
from ..util import load_object


class OTPMiddleware(MiddlewareMixin):
    """
    OTPMiddleware 中间件优化，添加 otp_confirmed_devices
    """

    otp_not_required_key = OTP_NOT_REQUIRED_KEY

    default_otp_device = None

    def process_request(self, request):
        """
        获取用户已验证的OTP设备
        :param request:
        :return:
        """

        try:
            request.user.otp_device = self.__get_user_otp_device(request=request)
        except OperationalError:
            self.close_old_connections()
            request.user.otp_device = self.__get_user_otp_device(request=request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        视图验证，无otp验证时，重定向到OPT验证页面
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """

        try:
            return self.__opt_check(request=request, view_func=view_func, view_args=view_args, view_kwargs=view_kwargs)
        except OperationalError:
            self.close_old_connections()
            return self.__opt_check(request=request, view_func=view_func, view_args=view_args, view_kwargs=view_kwargs)

    def __opt_check(self, request, view_func, view_args, view_kwargs):
        """
        视图验证，无otp验证时，重定向到OPT验证页面
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """
        allowed_view_func = [(load_object(i) if isinstance(i, str) else i) for i in settings.ALLOWED_VIEW_FUNC]
        if request.user.is_authenticated \
                and (view_func not in allowed_view_func) \
                and (not getattr(view_func, self.otp_not_required_key, False)) \
                and (not DeviceManage.is_otp_verified(request, request.user)):
            return HttpResponseRedirect(
                reverse('django_kelove_admin:otp_login') + '?next=' + urlquote(request.get_full_path())
            )

    def __get_user_otp_device(self, request):
        """
        获取用户OTP设备信息
        :param request:
        :return:
        """

        if not request.user.is_authenticated:
            return self.default_otp_device
        else:
            return DeviceManage.get_user_device(request, request.user)

    @staticmethod
    def close_old_connections():
        """
        关闭旧的数据库链接
        :return:
        """

        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()
