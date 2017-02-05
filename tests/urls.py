# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_fine_uploader.urls import urlpatterns as django_fine_uploader_urls

urlpatterns = [
    url(r'^', include(django_fine_uploader_urls, namespace='django_fine_uploader')),
]
