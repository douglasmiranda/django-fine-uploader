from django.db import models
from django.contrib import admin
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

    def add_view(self, request, form_url='', extra_context=None):
        return super(type(self), self).add_view(request, form_url, extra_context)
