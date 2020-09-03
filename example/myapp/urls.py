from django.urls import path
from . import views


urlpatterns = [
    path('widget/', views.ExampleWidgetView.as_view(), name='widget'),
]
