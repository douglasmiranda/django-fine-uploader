# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name="django_fine_uploader"

urlpatterns = [
    url(r'^upload/$', views.FineUploaderView.as_view(), name='upload'),
    url(r'^delete(/(?P<uuid>[0-9a-f-]+))?$', views.FineUploaderDeleteView.as_view(), name='delete'),
]
