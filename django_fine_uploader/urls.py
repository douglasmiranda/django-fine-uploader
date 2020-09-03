# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name="django_fine_uploader"

urlpatterns = [
    path('upload/', views.FineUploaderView.as_view(), name='upload'),
    path('delete', views.FineUploaderDeleteView.as_view(), name='delete'),
    path('delete/<uuid:uuid>', views.FineUploaderDeleteView.as_view(), name='delete'),
]
