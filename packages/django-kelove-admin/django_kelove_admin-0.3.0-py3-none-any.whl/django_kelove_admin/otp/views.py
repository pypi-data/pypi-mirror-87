# ==================================================================
#       文 件 名: views.py
#       概    要: 视图
#       作    者: IT小强 
#       创建时间: 8/10/20 10:21 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlquote

from .device import DeviceManage
from .forms import KeloveOTPTokenForm
from .decorators import otp_required
from ..settings import EmailSettingsForm
from ..conf import settings


@otp_required(required=False)
def otp(request):
    """
    OTP 验证视图
    :param request:
    :return:
    """

    EmailSettingsForm.change_django_settings()

    next_url = urlquote(request.GET.get('next', reverse('admin:index')))

    try:
        login_url = reverse(getattr(settings, 'LOGIN_URL', 'admin:login'))
    except NoReverseMatch:
        login_url = reverse('admin:login')

    login_url = login_url + '?next=' + next_url

    if request.user.is_anonymous:
        return HttpResponseRedirect(login_url)

    post_data = request.POST

    form = KeloveOTPTokenForm(
        user=request.user,
        request=request,
        data=post_data
    )

    if request.method == 'POST' and form.is_valid():
        DeviceManage.otp_login(request, form.user.otp_device)
        return HttpResponseRedirect(next_url)

    return render(request, settings.OTP_LOGIN_TEMPLATE, {
        'form': form,
        'title': _('一次性密码验证'),
        'site_header': _('一次性密码验证'),
    })
