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
    url(r'^logout/$', logout, {'next_page': '/login/'}, name="logout"),
    url(r'^register/$', views.register, name="register"),

    url(r'^newequipment/$', views.newEquipment, name="newEq"),
    url(r'^addequipment/$', views.addEquipment, name="addEq"),
    url(r'^addmaintenance/$', views.addMaintenance, name="addMT"),
    url(r'^checklist/$', views.checkList, name="checklist"),
    url(r'^report/$', views.dailyReport, name="dailyreport"),

    url(r'^form/$', views.formTest, name="test"),
]
