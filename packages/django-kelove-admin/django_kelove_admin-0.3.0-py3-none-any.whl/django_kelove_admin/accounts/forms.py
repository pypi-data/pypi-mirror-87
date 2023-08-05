"""
forms.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-08-21 4:43 PM
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django_registration.forms import RegistrationForm as BaseRegistrationForm

from ..settings import EmailSettingsForm


class PasswordResetForm(BasePasswordResetForm):
    """
    重置密码表单
    """

    def send_mail(self, *args, **kwargs):
        EmailSettingsForm.change_django_settings()
        super().send_mail(*args, **kwargs)


class RegistrationForm(BaseRegistrationForm):
    """
    注册表单
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        EmailSettingsForm.change_django_settings()

    class Meta(BaseRegistrationForm.Meta):
        model = get_user_model()
