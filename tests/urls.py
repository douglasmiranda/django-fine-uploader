# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.urls import path, include

from django_fine_uploader.urls import urlpatterns as django_fine_uploader_urls

urlpatterns = [
    path('', include('django_fine_uploader.urls', namespace='django_fine_uploader')),
]
