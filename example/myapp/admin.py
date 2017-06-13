import os
import shutil

from django.db import models
from django.db.models import FileField
from django.contrib import admin
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile

# Class only used for denotation.
from django.http.request import HttpRequest

from .models import FineFile

from django_fine_uploader import widgets


@admin.register(FineFile)
class FineFileAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.FileField: {
            'widget': widgets.FineUploaderWidget(attrs={'admin': True, 'itemLimit': 1})
        },
    }

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
        )

    def fineuploader_setting(self, request: HttpRequest):
        post_info = request.POST.dict()
        if type(self.formfield_overrides.get(FileField).get('widget')) is widgets.FineUploaderWidget:
            model_fields = self.model._meta.fields
            file_fields = {}
            file_fields_name = []
            for field in model_fields:
                if field.get_internal_type() is 'FileField':
                    file_fields_name.append(field.name)
            if request.method == 'POST':
                print(file_fields_name)
                for name in file_fields_name:
                    file_uploader = cache.get(request.POST.get(name))
                    file_path = file_uploader.storage.path(file_uploader.real_path)
                    post_info[name] = SimpleUploadedFile(
                        file_uploader.filename,
                        open(file_path, 'rb').read()
                    )
                    request.POST = post_info
                    folder_path = file_uploader.storage.path(file_uploader.file_path)
                    try:
                        shutil.rmtree(folder_path)
                    except (OSError, PermissionError):
                        pass
        # return post_info

    def add_view(self, request, form_url='', extra_context=None):
        self.fineuploader_setting(request)
        return super(type(self), self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fineuploader_setting(request)
        return super(type(self), self).change_view(request, object_id, form_url, extra_context)
