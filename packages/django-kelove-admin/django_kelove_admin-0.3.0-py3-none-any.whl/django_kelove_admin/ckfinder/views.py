# ==================================================================
#       文 件 名: views.py
#       概    要: 视图
#       作    者: IT小强 
#       创建时间: 8/14/20 3:21 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import os

from ..conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .ckfinder import Ckfinder
from ..apps import DjangoKeloveAdminConfig
from ..settings import GlobalSettingsForm


def ckfinder(request):
    return render(request, 'kelove_admin/ckfinder.html', {
        "ck_finder_api_url": reverse('django_kelove_admin:ckfinder_api'),
        "ck_finder_api_display_folders_panel": 0
    })


@csrf_exempt
@login_required()
def ckfinder_api(request):
    global_ckfinder_settings = GlobalSettingsForm.get()

    file = {}
    file_obj = request.FILES.get('upload', None)
    if file_obj:
        file['name'] = file_obj.name
        file['file'] = file_obj.file

    rule_pre = DjangoKeloveAdminConfig.name + '.'

    rule = {
        "role": "*",
        "resourceType": "*",
        "folder": "/",
        'FOLDER_VIEW': request.user.has_perm(rule_pre + 'ck_finder_folder_view'),
        'FOLDER_CREATE': request.user.has_perm(rule_pre + 'ck_finder_folder_create'),
        'FOLDER_RENAME': request.user.has_perm(rule_pre + 'ck_finder_folder_rename'),
        'FOLDER_DELETE': request.user.has_perm(rule_pre + 'ck_finder_folder_delete'),
        'FILE_VIEW': request.user.has_perm(rule_pre + 'ck_finder_file_view'),
        'FILE_CREATE': request.user.has_perm(rule_pre + 'ck_finder_file_create'),
        'FILE_RENAME': request.user.has_perm(rule_pre + 'ck_finder_file_rename'),
        'FILE_DELETE': request.user.has_perm(rule_pre + 'ck_finder_file_delete'),
        'IMAGE_RESIZE': request.user.has_perm(rule_pre + 'ck_finder_image_resize'),
        'IMAGE_RESIZE_CUSTOM': request.user.has_perm(rule_pre + 'ck_finder_image_resize_custom'),
    }

    _ckfinder = Ckfinder(
        request.GET,
        request.POST,
        file,
        global_ckfinder_settings
    )

    response_data = _ckfinder.add_resource(
        adapter='django_kelove_admin.ckfinder.adapter.LocalAdapter',
        name='本地存储',
        path=os.path.join(settings.MEDIA_ROOT),
        url=settings.MEDIA_URL,
        allowedExtensions=list(global_ckfinder_settings.get('allowedExtensions', [])),
        deniedExtensions=list(global_ckfinder_settings.get('deniedExtensions', [])),
        maxSize=global_ckfinder_settings.get('maxSize', 52428800)
    ).add_rule(rule).run()

    if response_data['content_type'].lower() == 'application/json':
        response = JsonResponse(data=response_data['content'])
    else:
        response = HttpResponse(
            content=response_data['content'],
            content_type=response_data['content_type'],
        )
    response.status_code = response_data['status_code']

    for header_key, header_val in response_data['headers'].items():
        response[header_key] = header_val
    return response
