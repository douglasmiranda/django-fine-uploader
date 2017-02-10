# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload/$', views.FineUploaderView.as_view(), name='upload'),
]
