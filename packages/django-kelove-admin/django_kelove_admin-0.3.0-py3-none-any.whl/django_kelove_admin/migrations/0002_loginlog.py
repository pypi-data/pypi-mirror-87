# Generated by Django 3.1.3 on 2020-11-26 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_kelove_admin.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_kelove_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('action', models.IntegerField(choices=[(1, '登录成功'), (0, '登录失败')], default=0, verbose_name='日志类型')),
                ('agent', models.TextField(blank=True, default='', verbose_name='代理信息')),
                ('area', models.CharField(blank=True, default='', max_length=191, verbose_name='地域信息')),
                ('ip', models.GenericIPAddressField(blank=True, default=None, null=True, verbose_name='IP')),
                ('content', models.TextField(blank=True, default='', verbose_name='日志详情')),
                ('login_user', models.ForeignKey(blank=True, db_constraint=False, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='django_kelove_admin_loginlog_login_user_set', to=settings.AUTH_USER_MODEL, verbose_name='登录用户')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
            },
            managers=[
                ('objects', django_kelove_admin.models.LoginLogManager()),
            ],
        ),
    ]
