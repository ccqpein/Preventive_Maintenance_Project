from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

app_name = "PM"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^result/(?P<serial_num>.*)$', views.result, name="result"),
    url(r'^login/$', login, name="login"),
]
