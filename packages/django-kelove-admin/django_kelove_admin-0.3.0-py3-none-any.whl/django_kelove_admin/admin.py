# ==================================================================
#       文 件 名: admin.py
#       概    要: 后台管理
#       作    者: IT小强 
#       创建时间: 8/6/20 5:50 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from import_export.admin import ImportExportMixin, ExportMixin
from import_export.resources import ModelResource
from import_export import fields
from import_export.widgets import JSONWidget, CharWidget

from mptt.admin import MPTTModelAdmin

from . import models
from . import SettingsRegister
from .settings import SettingsForm
from .util import load_object
from .conf import settings


class ModelAdmin(admin.ModelAdmin):
    """
    后台管理基类
    """


class ModelAdminWithUser(ModelAdmin):
    """
    后台管理基类（自动写入创建用户ID和更新用户ID）
    """

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        自动写入创建用户ID和更新用户ID
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        if request.user:
            user = request.user
            obj.updated_user = user
            if not change:
                obj.created_user = user
        super().save_model(request, obj, form, change)


class ModelAdminMPTT(MPTTModelAdmin):
    """
    后台管理基类(支持树形结构)
    """


class ModelAdminMPTTWithUser(ModelAdminWithUser, ModelAdminMPTT):
    """
     后台管理基类(支持树形结构)（自动写入创建用户ID和更新用户ID）
    """


class SettingsImportExportResource(ModelResource):
    """
    配置导入导出处理类
    """

    settings_key = fields.Field(
        column_name='配置标识',
        attribute='settings_key',
        default='',
        saves_null_values=False,
        widget=CharWidget()
    )

    settings_title = fields.Field(
        column_name='配置名称',
        attribute='settings_title',
        default='',
        saves_null_values=False,
        widget=CharWidget()
    )

    settings_val = fields.Field(
        column_name='配置内容',
        attribute='settings_val',
        saves_null_values=False,
        widget=JSONWidget()
    )

    class Meta:
        fields = ['settings_key', 'settings_title', 'settings_val']
        import_id_fields = ['settings_key']
        use_transactions = True
        model = models.Settings


@admin.register(models.LoginLog)
class LoginLog(ExportMixin, ModelAdmin):
    """
    登录日志
    """

    list_display = (
        'login_user',
        'login_time',
        'action',
        'ip',
        'area',
        'agent',
    )

    list_display_links = (
        'login_user',
        'login_time',
        'action'
    )

    search_fields = ('ip', 'area', 'agent', 'content')

    list_filter = ('action', 'login_time')

    def has_add_permission(self, request):
        # 禁用添加
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除
        return False

    def has_change_permission(self, request, obj=None):
        # 禁止修改
        return False


@admin.register(models.Settings)
class Settings(ImportExportMixin, ModelAdminWithUser):
    """
    配置管理
    """

    resource_class = SettingsImportExportResource

    list_display = (
        'id',
        'settings_title',
        'settings_key',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
    )

    list_display_links = ('settings_title', 'settings_key')

    list_filter = ('created_time', 'updated_time')

    search_fields = ('settings_title', 'settings_key')

    readonly_fields = ('settings_title', 'settings_key')

    def add_view(self, request, form_url='', extra_context=None):
        """
        初始化
        :param request:
        :param form_url:
        :param extra_context:
        :return:
        """

        for form in SettingsRegister.get():
            if isinstance(form, str):
                form = load_object(form)

            if not issubclass(form, SettingsForm):
                continue

            try:
                models.Settings.objects.create(
                    settings_key=form.get_settings_key(),
                    settings_title=form.get_settings_title(is_full=False),
                    settings_val=form.get(),
                    created_user=request.user,
                    updated_user=request.user
                )
                form.delete_cache()
            except IntegrityError:
                pass

        opts = self.model._meta
        obj_url = reverse(
            'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(obj_url)

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj:
            try:
                form = load_object(obj.settings_key)
                if issubclass(form, SettingsForm):
                    return form
            except AttributeError:
                pass
        return super().get_form(request, obj, change, **kwargs)

    class Media:
        css = {'all': ('kelove_admin/form.css',)}


if settings.REGISTER_PERMISSION_ADMIN:
    @admin.register(Permission)
    class PermissionAdmin(ImportExportMixin, ModelAdmin):
        """
        权限后台管理
        """

        list_display = (
            'id',
            'name',
            'content_type',
            'codename',
        )

        list_display_links = ('id', 'name')

        list_filter = ('content_type',)

        search_fields = ('name', 'codename')

if settings.REGISTER_CONTENT_TYPE_ADMIN:
    @admin.register(ContentType)
    class ContentTypeAdmin(ImportExportMixin, ModelAdmin):
        """
        内容类型后台管理
        """

        list_display = (
            'id',
            'app_label',
            'model',

        )

        list_display_links = ('id', 'app_label', 'model')

        search_fields = ('app_label', 'model')

if settings.REGISTER_LOG_ENTRY_ADMIN:
    @admin.register(LogEntry)
    class LogEntryAdmin(ImportExportMixin, ModelAdmin):
        """
        日志管理后端
        """

        list_display = (
            'id',
            'content_type',
            'object_id',
            'object_repr',
            'action_flag',
            'change_message',
            'action_time',
            'user',
        )

        list_display_links = ('id', 'content_type')

        list_filter = ('content_type', 'action_flag', 'action_time')

        search_fields = ('change_message', 'object_repr')
