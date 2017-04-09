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
    url(r'^report/$', views.dailyReport, name="dailyreport"),
    url(r'^order/$', views.orderRequest, name="order"),
    url(r'^viewMain/(?P<form_ID>[0-9]+)/$', views.viewMain, name="viewMT"),
    url(r'^viewTasks/$', views.viewTasks, name="viewTasks"),
    url(r'^viewOrders/(?P<orderNumber>[0-9]+)/$',
        views.viewOrders, name="viewOrders"),
    url(r'^viewEq/(?P<eqNumber>[0-9]+)/$', views.viewEq, name="viewEq"),

    url(r'^form/$', views.formTest, name="test"),
]
