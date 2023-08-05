# ==================================================================
#       文 件 名: urls.py
#       概    要: 路由
#       作    者: IT小强 
#       创建时间: 8/10/20 11:06 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.urls import path
from django.contrib.auth.views import PasswordResetView
from django_registration.views import RegistrationView

from .apps import DjangoKeloveAdminConfig
from .otp.views import otp
from .ckfinder.views import ckfinder, ckfinder_api
from .accounts.forms import PasswordResetForm, RegistrationForm

# 修改重置密码视图的表单类
PasswordResetView.form_class = PasswordResetForm
# 修改注册视图的表单类
RegistrationView.form_class = RegistrationForm

app_name = DjangoKeloveAdminConfig.name

urlpatterns = [
    # OPT 验证
    path('otp-login/', otp, name='otp_login'),

    # ckfinder
    path('ckfinder/', ckfinder, name='ckfinder'),
    path('ckfinder-api/', ckfinder_api, name='ckfinder_api'),
]
