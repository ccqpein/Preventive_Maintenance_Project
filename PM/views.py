from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect

# Create your views here.
# from django.contrib.auth.models import User
from .models import Equipment, MyUser
from .forms import RegisterFrom


@login_required(login_url="/login/")
def index(request):
    return render(request, 'PM/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterFrom(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(username=form.data["username"],
                                              first_name=form.data["f_name"],
                                              last_name=form.data["l_name"],
                                              email=form.data["email"],
                                              phone=form.data["phone"],
                                              password=form.data["passw"],
                                              note=form.data["note"])
            user.save()
            return HttpResponseRedirect("/login/")
    else:
        form = RegisterFrom()
    return render(request, "registration/register.html", {'form': form})


@login_required(login_url="/login/")
@permission_required('PM.view_Equipment', login_url='/login/')
def result(request, serial_num):
    serial_num = request.GET['serialNum']
    equipment = get_object_or_404(Equipment, eq_serial_num=serial_num)
    return render(request, 'PM/result.html', {
        'serial_number': serial_num,
        'object_name': equipment.eq_name,
        'left': equipment.eq_quantity_left,
    })


@login_required(login_url="/login/")
def newEquipment(request):
    return render(request, 'PM/NewEquipment.html')


@login_required(login_url="/login/")
# @permission_required('PM.view_Equipment', login_url='/login/')
def addEquipment(request):
    data = request.POST

    print(data['warranty_expir_date'])
    eq = Equipment(
        eq_serial_num=data['serial_num'],
        eq_name=data['name'],
        eq_type=data['type'],
        eq_expir_date=data['warranty_expir_date'],
        eq_purchase_date=data['purchase_date'],
        eq_manufacturer=data['manufacturer_date'],
        eq_internal_part_num=data['internal_part_num'],
        eq_contact_notes=data['note'],
        eq_maintenance_schedule=data['schedule'],
    )
    eq.save()

    return render(request, 'PM/message.html', {'message': "save successful"})


@login_required(login_url="/login/")
def addMaintenance(request):
    if not request.GET:
        return render(request, 'PM/NewMaintenance.html', {'lalala': [2, 3, 4]})


@login_required(login_url="/login/")
def checkList(request):
    if not request.GET:
        return render(request, 'PM/CheckList.html')
    else:
        print("get")
        return render(request, 'PM/CheckList.html')


@login_required(login_url="/login/")
def dailyReport(request):
    if not request.GET:
        return render(request, 'PM/dailyReport.html')
    else:
        return render(request, 'PM/dailyReport.html')


@login_required(login_url="/login/")
def orderRequest(request):
    if not request.GET:
        return render(request, 'PM/order.html')
    else:
        return render(request, 'PM/order.html')


def formTest(request):
    return render(request, 'PM/forms.html')
