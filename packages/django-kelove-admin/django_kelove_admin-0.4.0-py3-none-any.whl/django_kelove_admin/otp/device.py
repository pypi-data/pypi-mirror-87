"""
OTP设备验证管理
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-08-21 1:56 PM
"""

from django.core.cache import cache
from ..conf import settings
from django_otp import DEVICE_ID_SESSION_KEY, devices_for_user
from django_otp.middleware import is_verified
from django_otp.models import Device


class DeviceManage:
    """
    OTP设备验证管理类
    """

    # 缓存标签
    CACHE_KEY = 'cache_' + DEVICE_ID_SESSION_KEY

    @classmethod
    def otp_login(cls, request, user_device=None):
        """
        OTP 验证登录回调
        :param request:
        :param user_device:
        :return:
        """

        _user = getattr(request, 'user', None)
        if not user_device:
            if hasattr(_user, 'otp_device'):
                user_device = _user.otp_device

        if (_user is not None) and (user_device is not None) and (user_device.user_id == _user.pk):
            cache.set(cls.CACHE_KEY + str(_user.pk), user_device.persistent_id, settings.SESSION_COOKIE_AGE)
            request.session[DEVICE_ID_SESSION_KEY] = user_device.persistent_id

    @classmethod
    def otp_logout(cls, request, user):
        """
        OTP 退出登录回调
        :param request:
        :param user:
        :return:
        """

        # 删除session
        cls._del_otp_device_persistent_id_form_session(request, user)
        # 删除cache
        cls._del_otp_device_persistent_id_form_cache(request, user)

    @classmethod
    def is_otp_verified(cls, request, user):
        """
        检查用户是否已经验证过一次性验证码
        :param request:
        :param user:
        :return:
        """

        # 根据用户是否有otp设备来决定是否进行otp权限验证
        devices = devices_for_user(user=user, confirmed=True)
        try:
            device = next(devices)
        except (StopIteration, TypeError):
            device = None

        # 有可用设备时正常验证
        if device is not None:
            return is_verified(user)

        # 没有可用设备时不验证，直接返回True
        return True

    @classmethod
    def get_user_device(cls, request, user):
        """
        获取当前用户已经验证的OTP设备
        """
        persistent_id = DeviceManage.get_otp_device_persistent_id(request, user)

        device = cls.device_from_persistent_id(persistent_id) if persistent_id else None

        if (device is not None) and (device.user_id != user.pk):
            device = None

        if device is None:
            cls._del_otp_device_persistent_id_form_session(request, user)
            cls._del_otp_device_persistent_id_form_cache(request, user)

        return device

    @classmethod
    def device_from_persistent_id(cls, persistent_id):
        # Convert legacy persistent_id values (these used to be full import
        # paths). This won't work for apps with models in sub-modules, but that
        # should be pretty rare. And the worst that happens is the user has to
        # log in again.
        if persistent_id.count('.') > 1:
            parts = persistent_id.split('.')
            persistent_id = '.'.join((parts[-3], parts[-1]))

        device = Device.from_persistent_id(persistent_id)

        return device

    @classmethod
    def get_otp_device_persistent_id(cls, request, user):
        """
        获取 otp_device_persistent_id
        :param request:
        :param user:
        :return:
        """

        # 首先查询 session 中是否存在 persistent_id
        persistent_id = cls._get_otp_device_persistent_id_form_session(request, user)
        if persistent_id:
            return persistent_id
        persistent_id = cls._get_otp_device_persistent_id_form_cache(request, user)
        if persistent_id:
            return persistent_id
        return None

    @classmethod
    def _get_otp_device_persistent_id_form_session(cls, request, user):
        """
        从 session 中获取 device_persistent_id
        :param request:
        :param user:
        :return:
        """

        persistent_id = request.session.get(DEVICE_ID_SESSION_KEY)
        if persistent_id:
            return persistent_id
        return None

    @classmethod
    def _del_otp_device_persistent_id_form_session(cls, request, user):
        """
        从session中删除device_persistent_id
        :param request:
        :param user:
        :return:
        """

        if DEVICE_ID_SESSION_KEY in request.session:
            del request.session[DEVICE_ID_SESSION_KEY]

    @classmethod
    def _get_otp_device_persistent_id_form_cache(cls, request, user):
        """
        从 session 中获取 device_persistent_id
        :param request:
        :param user:
        :return:
        """

        user_id = getattr(user, 'id', getattr(user, 'pk', None))
        if not user_id:
            return None

        persistent_id = cache.get(cls.CACHE_KEY + str(user_id))
        if persistent_id:
            return persistent_id

        return None

    @classmethod
    def _del_otp_device_persistent_id_form_cache(cls, request, user):
        """
        从session中删除device_persistent_id
        :param request:
        :return:
        """

        user_id = getattr(user, 'id', getattr(user, 'pk', None))
        if user_id:
            cache.delete(cls.CACHE_KEY + str(user_id))
