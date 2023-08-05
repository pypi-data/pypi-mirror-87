"""
settings.py 配置管理
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-08-10 4:23 PM
"""

import json
from hashlib import md5

from django import forms
from django.core.cache import cache
from django.db import ProgrammingError, OperationalError
from django.utils.translation import gettext_lazy as _
from django.conf import settings as django_settings

from .models import Settings


class SettingsForm(forms.ModelForm):
    """
    配置表单基类
    """

    settings_title: str = _('未命名')

    settings_val = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, data=None, files=None, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)
        kwargs['initial'] = {
            **initial,
            **self.init_form_initial(instance=instance)
        }
        super().__init__(data=data, files=files, **kwargs)

    def clean(self):
        settings_val = self.get()
        for key, val in self.cleaned_data.items():
            if key != 'settings_val' and key in self.changed_data:
                settings_val[key] = val

        self.cleaned_data['settings_val'] = settings_val
        return super().clean()

    def init_form_data(self, data=None, instance=None):
        """
        初始化表单数据
        :param data:
        :param instance:
        :return:
        """

        # 表单数据已存在时，不做处理
        if data is not None:
            return data
        return self.init_form_initial(instance=instance)

    def init_form_initial(self, instance=None):
        """
        初始化表单初始值
        :param instance:
        :return:
        """

        data = {}

        if not instance:
            return data

        # 查询结果转为字典
        instance_data = forms.model_to_dict(instance)

        # 循环处理配置值
        settings_val = instance_data.get('settings_val', {})
        if not settings_val:
            settings_val = {}
        if isinstance(settings_val, str):
            try:
                settings_val = json.loads(settings_val)
            except json.JSONDecodeError:
                settings_val = {}

        for field_name, field_info in self.base_fields.items():
            if field_name == 'settings_val':
                continue
            try:
                data[field_name] = settings_val.get(field_name, self.get_initial(field_info))
            except AttributeError:
                pass

        data['settings_key'] = instance_data['settings_key']
        data['settings_title'] = instance_data['settings_title']
        return data

    @classmethod
    def get_settings_key(cls):
        """
        获取当前配置类标识
        :return:
        """

        return '{module}.{name}'.format(
            module=cls.__module__,
            name=cls.__name__
        )

    @classmethod
    def get_settings_title(cls, is_full=True):
        """
        获取当前配置类名称
        :param is_full:
        :return:
        """

        if not is_full:
            return cls.settings_title
        return '{base_name}【{module}.{name}】'.format(
            base_name=cls.settings_title,
            module=cls.__module__,
            name=cls.__name__
        )

    @classmethod
    def get_cache_key(cls):
        """
        获取缓存标识
        :return:
        """

        return 'settings_{file}_{key}_cache'.format(
            file=md5(__file__.encode()).hexdigest(),
            key=md5(cls.get_settings_key().encode()).hexdigest()
        )

    @classmethod
    def delete_cache(cls):
        """
        删除缓存
        :return:
        """

        cache_key = cls.get_cache_key()
        cache.delete(cache_key)

    @classmethod
    def get(cls) -> dict:
        """
        获取配置
        :return:
        """

        cache_key = cls.get_cache_key()
        cache_data = cache.get(cache_key)
        if cache_data is None:
            try:
                data = Settings.objects.get(settings_key=cls.get_settings_key())
                data = data.settings_val
            except (Settings.DoesNotExist, ProgrammingError, OperationalError):
                data = {}
            initial_data = {}
            for key, val in cls.base_fields.items():
                if key == 'settings_val':
                    continue
                try:
                    initial_data[key] = cls.get_initial(val)
                except AttributeError:
                    pass
            cache_data = {**initial_data, **data}
            cache.set(cache_key, cache_data)

        return cache_data

    @classmethod
    def get_initial(cls, field):
        """
        获取初始值
        :param field:
        :return:
        """

        value = getattr(field, 'initial')
        if callable(value):
            value = value()
        return value

    @classmethod
    def get_initial_with_default(cls, field, default):
        """
        获取初始值，不存在时返回 default
        :param field:
        :param default:
        :return:
        """

        value = getattr(field, 'initial', default)
        if callable(value):
            value = value()
        return value

    @classmethod
    def change_django_settings(cls):
        """
        刷新django设置
        :return:
        """

        for key, val in cls.get().items():
            setattr(django_settings, key, val)

    def update_choices(self, field, value):
        """
        动态更新可选项
        :param field:
        :param value:
        :return:
        """
        self.fields[field].choices = value
        self.fields[field].widget.choices = value
        self.base_fields[field].choices = value
        self.base_fields[field].widget.choices = value

    def save(self, commit=True):
        self.delete_cache()
        return super().save(commit)

    class Meta:
        """
        Meta
        """

        model = Settings
        fields = ['settings_val']


class GlobalSettingsForm(SettingsForm):
    """
    全局配置
    """

    from .forms.fields import JSONField

    settings_title: str = _('全局配置')

    ckfinder_selector_settings = JSONField(
        initial={
            'displayFoldersPanel': True,
            'license_name': '',
            'license_key': '',
            'allowedExtensions': [],
            'deniedExtensions': [],
            'maxSize': 52428800,
        },
        label=_('CKFinder文件管理器配置'),
        required=False,
        field_settings={
            "mode": "code",
            "modes": ["code", "tree"],
        },
    )

    markdown_editor_settings = JSONField(
        initial={
            "imageUpload": True,
            "imageUploadURL": {}
        },
        label=_('Markdown编辑器配置'),
        required=False,
        field_settings={
            "mode": "code",
            "modes": ["code", "tree"],
        }
    )


class EmailSettingsForm(SettingsForm):
    """
    邮件配置
    """

    settings_title: str = _('邮件配置')

    EMAIL_HOST = forms.CharField(
        initial=getattr(django_settings, 'EMAIL_HOST', 'smtp.qq.com'),
        empty_value=getattr(django_settings, 'EMAIL_HOST', 'smtp.qq.com'),
        required=False,
        label=_('邮件服务器域名'),
        help_text=_('例如：smtp.qq.com')
    )

    EMAIL_PORT = forms.IntegerField(
        initial=getattr(django_settings, 'EMAIL_PORT', 465),
        required=False,
        label=_('邮件服务器端口号，为数字'),
        help_text=_('例如：465')
    )

    EMAIL_HOST_USER = forms.CharField(
        initial=getattr(django_settings, 'EMAIL_HOST_USER', ''),
        required=False,
        label=_('发件人邮箱'),
    )

    DEFAULT_FROM_EMAIL = forms.CharField(
        initial=getattr(django_settings, 'DEFAULT_FROM_EMAIL', ''),
        required=False,
        label=_('发件人地址'),
        help_text=_('fred@example.com 和 Fred &lt;fred@example.com&gt; 形式都是合法的')
    )

    OTP_EMAIL_SENDER = forms.CharField(
        initial=getattr(django_settings, 'OTP_EMAIL_SENDER', ''),
        required=False,
        label=_('一次性验证码发件人地址'),
        help_text=_('留空自动使用发件人地址。fred@example.com 和 Fred &lt;fred@example.com&gt; 形式都是合法的')
    )

    EMAIL_HOST_PASSWORD = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        initial=getattr(django_settings, 'EMAIL_HOST_PASSWORD', ''),
        required=False,
        label=_('发件人授权码'),
        help_text=_('发件人授权码不一定是邮箱密码')
    )

    EMAIL_USE_TLS = forms.BooleanField(
        initial=getattr(django_settings, 'EMAIL_USE_TLS', False),
        required=False,
        label=_('是否启用安全链接TLS'),
        help_text=_('通常端口为587 TLS/SSL是相互排斥的，因此仅将其中一个设置设置为启用即可')
    )

    EMAIL_USE_SSL = forms.BooleanField(
        initial=getattr(django_settings, 'EMAIL_USE_SSL', True),
        required=False,
        label=_('是否启用安全链接SSL'),
        help_text=_('通常端口为465 TLS/SSL是相互排斥的，因此仅将其中一个设置设置为启用即可')
    )

    @classmethod
    def get(cls) -> dict:
        data = super().get()
        otp_email_sender_value = data.get('OTP_EMAIL_SENDER', '')
        if not otp_email_sender_value:
            otp_email_sender_value = data.get('DEFAULT_FROM_EMAIL', '')
        data['OTP_EMAIL_SENDER'] = otp_email_sender_value
        return data
