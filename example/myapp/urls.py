from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^widget/$', view=views.ExampleWidgetView.as_view()),
]
