from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect

# Create your views here.
# from django.contrib.auth.models import User
from .models import Equipment, MyUser
from .forms import RegisterFrom


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
    equipment = get_object_or_404(Equipment, serial_num=serial_num)
    return render(request, 'PM/result.html', {
        'serial_number': serial_num,
        'object_name': equipment.name,
        'left': equipment.quantity_left,
    })
