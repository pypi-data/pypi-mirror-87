# ==================================================================
#       文 件 名: forms.py
#       概    要: 表单
#       作    者: IT小强 
#       创建时间: 8/10/20 10:23 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================


from django import forms
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from django_otp.forms import OTPTokenForm


class KeloveOTPTokenForm(OTPTokenForm):
    """
    OTP TOKEN 验证表单
    """

    otp_error_messages = {
        'token_required': _('Please enter your OTP token.'),
        'challenge_exception': _('Error generating challenge: {0}'),
        'not_interactive': _('The selected OTP device is not interactive'),
        'challenge_message': _('OTP Challenge: {0}'),
        'invalid_token': _('Invalid token. Please make sure you have entered it correctly.'),
        'n_failed_attempts': ngettext_lazy(
            "Verification temporarily disabled because of %(failure_count)d failed attempt, please try again soon.",
            "Verification temporarily disabled because of %(failure_count)d failed attempts, please try again soon.",
            "failure_count"),
        'verification_not_allowed': _("Verification of the token is currently disabled"),
    }

    otp_device = forms.ChoiceField(
        choices=[],
        label=_('一次性密码设备')
    )

    otp_token = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        label=_('一次性密码')
    )

    otp_challenge = forms.BooleanField(
        required=False,
        initial=False,
        label=_('获取一次性密码'),
        help_text=_('仅交互式设备可用（如：邮件或短信验证码）')
    )
