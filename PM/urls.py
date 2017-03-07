from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

app_name = "PM"


def login_remember(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)
    return login(request, *args, **kwargs)

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^result/(?P<serial_num>.*)$', views.result, name="result"),
    url(r'^login/$', login_remember, name="login"),
    url(r'^register/$', views.register, name="register"),
]
