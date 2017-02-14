from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.
from .models import Equipment


def index(request):
    return render(request, 'PM/index.html')


# @permission_required('check_perm', login_url='/login/')
@login_required(login_url="/query/login/")
def result(request, serial_num):
    serial_num = request.GET['serialNum']
    equipment = get_object_or_404(Equipment, serial_num=serial_num)
    return render(request, 'PM/result.html', {
        'serial_number': serial_num,
        'object_name': equipment.name,
        'left': equipment.quantity_left,
    })
