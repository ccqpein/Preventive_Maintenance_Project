from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

# Create your views here.
# from django.contrib.auth.models import User
from .models import Equipment, EquipmentTool, DailyReport, Order, MyUser, MaintenanceContent, MaintenanceSchedule
from .forms import RegisterFrom
from datetime import datetime, timedelta


def taskLeft(time):
    resultList = []
    od = Order.objects.filter(ord_complete=False)

    if time == 'today':
        eq = Equipment.objects.filter(
            eq_next_main_date=datetime.today())
        mainT = MaintenanceSchedule.objects.filter(
            ms_next_main_date=datetime.today())
        for c in od:
            resultList.append(
                ("Work Order", c.ord_date, "", "/viewOrders/" + str(c.id) + "/"))

        for c in eq:
            resultList.append(("Equipment", c.eq_add_date, "Today",
                               "/viewEq/" + str(c.id) + "/"))

        for c in mainT:
            resultList.append(("Maintenance", c.ms_date, "Today",
                               "/viewMain/" + str(c.id) + "/"))

    else:
        eq = Equipment.objects.filter(
            eq_next_main_date__range=(datetime.today() + timedelta(days=1),
                                      datetime.today() + timedelta(weeks=4)))
        mainT = MaintenanceSchedule.objects.filter(
            ms_next_main_date__range=(datetime.today() + timedelta(days=1),
                                      datetime.today() + timedelta(weeks=4)))
        for c in eq:
            resultList.append(("Equipment", c.eq_add_date, c.eq_next_main_date,
                               "/viewEq/" + str(c.id) + "/"))

        for c in mainT:
            resultList.append(("Maintenance", c.ms_date, c.ms_next_main_date,
                               "/viewMain/" + str(c.id) + "/"))

    return resultList


@login_required(login_url="/login/")
def index(request):
    orderLeft = Order.objects.filter(ord_complete=False).count()
    equipmentLeft = len(Equipment.objects.all())
    maintenanceLeft = len(MaintenanceSchedule.objects.all())
    if not request.user.is_staff:
        dailyReportLeft = len(DailyReport.objects.filter(
            dp_date=datetime.today(), dp_user=request.user))
    else:
        dailyReportLeft = len(DailyReport.objects.filter(
            dp_date=datetime.today()))
    tasks = taskLeft('today')
    print(request.user)
    return render(request, 'PM/index.html',
                  {'order_left': orderLeft,
                   'eq_left': equipmentLeft,
                   'mainLeft': maintenanceLeft,
                   'dpLeft': dailyReportLeft,
                   'all_left': len(tasks)}
                  )


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
        eq_manufacturer=data['manufacturer'],
        eq_internal_part_num=data['internal_part_num'],
        eq_contact_notes=data['note'],
        eq_maintenance_schedule=data['schedule'],
        eq_quantity_left=data['quantity_left']
    )
    eq.save()

    return render(request, 'PM/message.html', {'message': "save successful"})


@login_required(login_url="/login/")
@permission_required('PM.view_Equipment', login_url='/login/')
def addMaintenance(request):
    if request.method != 'GET':
        data = request.POST
        print(data)
        ms = MaintenanceSchedule(
            ms_name=data['name'],
            ms_serial_num=data['serial_num'],
            ms_inter_part=data['internal_part_num'],

            ms_tools_name=" -*- ".join(request.POST.getlist('ToolName')),
            ms_tools_qty=" -*- ".join(request.POST.getlist('ToolQty')),

            ms_form_names=" -*- ".join(request.POST.getlist('mfname')),
            ms_form_reqs=" -*- ".join(request.POST.getlist('mfreq')),
            ms_form_fields=" -*- ".join(request.POST.getlist('mffieldtype')),
            ms_maintenance_schedule=data['schedule'],
        )
        dt = datetime.today() + \
            timedelta(int(data['schedule']) * 7)
        ms.ms_next_main_date = datetime(dt.year, dt.month, dt.day)
        ms.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})
    else:
        tools = [i.tool_name for i in EquipmentTool.objects.all()]
        return render(request, 'PM/NewMaintenance.html',
                      {'toolnames': tools, })


def viewMain(request, form_ID):
    if request.method != 'GET':
        data = request.POST
        print(data)
        ms = MaintenanceSchedule.objects.get(
            id=form_ID)
        mc = MaintenanceContent(
            mc_temp=ms,
            mc_content=" -*- ".join(request.POST.getlist('values')),
        )
        mc.save()

        ms.ms_last_main_date = datetime.today()
        dt = datetime.today() + timedelta(ms.ms_maintenance_schedule * 7)
        ms.ms_next_main_date = datetime(dt.year, dt.month, dt.day)
        ms.save()

        return render(request, 'PM/message.html',
                      {'message': "submit successful"})
    else:
        lines = model_to_dict(get_object_or_404(
            MaintenanceSchedule, id=form_ID))
        print(lines)

        temp = [('ms_name', lines['ms_name']),
                ('serial number', lines['ms_serial_num']),
                ('internal part number', lines['ms_inter_part']), ]

        toolstemp = [(lines['ms_tools_name'].split(' -*- ')),
                     (lines['ms_tools_qty'].split(' -*- ')),
                     ]
        toolstemp = list(zip(toolstemp[0], toolstemp[1]))

        labels = lines['ms_form_names'].split(' -*- ')
        labels = list(filter(lambda x: x != '' and x != ' -*-', labels))
        reqs = lines['ms_form_reqs'].split(' -*- ')
        types = lines['ms_form_fields'].split(' -*- ')
        MT = [(labels[i], reqs[i], types[i]) for i in range(len(labels))]

        print(MT)
        return render(request, 'PM/Maintenance.html',
                      {'MT': MT,
                       'form_ID': form_ID,
                       'toolstemp': toolstemp,
                       'mainName': lines['ms_name'],
                       'temp': temp})


@login_required(login_url="/login/")
@permission_required('PM.add_dailyreport', login_url='/login/')
def dailyReport(request):
    if request.method != 'GET':
        data = request.POST
        dr = DailyReport(
            dp_name=data['name'],
            dp_shift=data['shift'],
            dp_date=data['date'],
            dp_work_performed=data['workperformed'],
            dp_problems_ident=data['problems'],
            dp_user=request.user,
        )
        dr.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})
    else:
        return render(request, 'PM/dailyReport.html')


@login_required(login_url="/login/")
@permission_required('PM.add_order', login_url='/login/')
def orderRequest(request):
    if request.method != 'GET':
        data = request.POST
        print(data)
        od = Order(
            ord_date=data['dateReq'],
            ord_req_by=data['reqBy'],
            ord_building=data['building'],
            ord_floor=data['floor'],
            ord_room=data['room'],
            ord_supervisor=data['supervisor'],
            ord_work_req=data['workrequested'],
            ord_work_ord=data['workOrder'],
            ord_date_issue=data['dateIssued'],
            ord_employee=data['employee'],
            ord_comments=data['materialsused'],
        )

        od.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})
    else:
        return render(request, 'PM/order.html')


def viewTasks(request):
    if request.method == 'GET':
        resultList = taskLeft(time='today')
        resultList2 = taskLeft(time='whatever')
        return render(request, 'PM/viewForm.html',
                      {'titles': ["Type", "Add Date", 'Due Date', 'View'],
                       'content': resultList + resultList2})


def viewOrders(request, orderNumber):
    if request.method == 'GET':
        od = Order.objects.get(id=orderNumber)
        checkMark = ""
        if od.ord_complete:
            checkMark = "checked"
        return render(request, 'PM/viewOrders.html',
                      {'dateReq': od.ord_date,
                       'reqBy': od.ord_req_by,
                       'building': od.ord_building,
                       'floor': od.ord_floor,
                       'room': od.ord_room,
                       'supervisor': od.ord_supervisor,
                       'workrequested': od.ord_work_req,
                       'workOrder': od.ord_work_ord,
                       'dateIssued': od.ord_date_issue,
                       'employee': od.ord_employee,
                       'materialsused': od.ord_comments,
                       'orderNumber': orderNumber,
                       'complete': checkMark,
                       })
    else:
        od = Order.objects.get(id=orderNumber)
        print(request.POST)
        if request.POST.get('complete'):
            od.ord_complete = True
        else:
            od.ord_complete = False
        od.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})


def viewEq(request, eqNumber):
    if request.method == 'GET':
        eq = Equipment.objects.get(id=eqNumber)
        content = {'eqNumber': eqNumber,
                   'name': eq.eq_name,
                   'serial_num': eq.eq_serial_num,
                   'type': eq.eq_type,
                   'warranty': eq.eq_expir_date,
                   'purchase': eq.eq_purchase_date,
                   'manufacturer': eq.eq_manufacturer,
                   'internal_part_num': eq.eq_internal_part_num,
                   'schedule': eq.eq_maintenance_schedule,
                   'note': eq.eq_contact_notes, }

        return render(request, 'PM/viewEquipment.html',
                      content)
    else:
        eq = Equipment.objects.get(id=eqNumber)
        eq.eq_last_main_date = datetime.today()
        dt = datetime.today() + timedelta(eq.eq_maintenance_schedule * 7)
        eq.eq_next_main_date = datetime(dt.year, dt.month, dt.day)
        eq.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})


def formTest(request):
    return render(request, 'PM/viewForm.html',
                  {'titles': [1, 2, 3, 4, 5],
                   'content': [(11, 22, 33, 44)]})
