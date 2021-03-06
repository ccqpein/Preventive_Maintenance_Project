from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

# Create your views here.
# from django.contrib.auth.models import User
from .models import Equipment, EquipmentTool, DailyReport, Order, MyUser, MaintenanceContent, MaintenanceSchedule
from datetime import datetime, timedelta
import random


def taskLeft(time, request):
    resultList = []
    od = Order.objects.filter(ord_complete=False)

    if time == 'today':
        eq = Equipment.objects.filter(
            eq_next_main_date=datetime.today())
        mainT = MaintenanceSchedule.objects.filter(
            ms_next_main_date=datetime.today())
        for c in od:
            resultList.append(
                (c.ord_req_by + str(' (for you)' if c.ord_assign == request.user else ''), "Work Order", c.ord_date, "", "/viewOrders/" + str(c.id) + "/"))

        for c in eq:
            resultList.append(
                (c.eq_name, "Equipment", c.eq_add_date, "Today",
                 "/viewEq/" + str(c.id) + "/"))

        for c in mainT:
            resultList.append(
                (c.ms_name, "Maintenance", c.ms_date, "Today",
                 "/viewMain/" + str(c.id) + "/"))

    else:
        eq = Equipment.objects.filter(
            eq_next_main_date__range=(datetime.today() + timedelta(days=1),
                                      datetime.today() + timedelta(weeks=4)))
        mainT = MaintenanceSchedule.objects.filter(
            ms_next_main_date__range=(datetime.today() + timedelta(days=1),
                                      datetime.today() + timedelta(weeks=4)))
        for c in eq:
            resultList.append((c.eq_name, "Equipment", c.eq_add_date, c.eq_next_main_date,
                               "/viewEq/" + str(c.id) + "/"))

        for c in mainT:
            resultList.append((c.ms_name, "Maintenance", c.ms_date, c.ms_next_main_date,
                               "/viewMain/" + str(c.id) + "/"))

    return resultList


@login_required(login_url="/login/")
def index(request):
    orderLeft = Order.objects.filter(ord_complete=False).count()
    equipmentLeft = len(Equipment.objects.all())
    maintenanceLeft = len(MaintenanceSchedule.objects.all())
    eqtoolsLeft = len(EquipmentTool.objects.filter(
        tool_quantity_left__range=(0, 5)))

    if not request.user.is_staff:
        dailyReportLeft = len(DailyReport.objects.filter(
            dp_date=datetime.today(), dp_user=request.user))
    else:
        dailyReportLeft = len(DailyReport.objects.filter(
            dp_date=datetime.today()))
    tasks = taskLeft('today', request)

    return render(request, 'PM/index.html',
                  {'order_left': orderLeft,
                   'eq_left': equipmentLeft,
                   'mainLeft': maintenanceLeft,
                   'dpLeft': dailyReportLeft,
                   'all_left': len(tasks),
                   'toolalarm': eqtoolsLeft}
                  )


@login_required(login_url="/login/")
def newEquipment(request):
    tools = [i.tool_name for i in EquipmentTool.objects.all()]
    return render(request, 'PM/NewEquipment.html',
                  {'toolnames': tools})


@login_required(login_url="/login/")
@permission_required('PM.add_equipment', login_url='/login/')
def addEquipment(request):
    data = request.POST

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
        eq_quantity_left=data['quantity_left'],

        eq_tools_name=" -*- ".join(request.POST.getlist('ToolName')),
        eq_tools_qty=" -*- ".join(request.POST.getlist('ToolQty')),
    )

    dt = datetime.today() + \
        timedelta(int(data['schedule']) * 7)
    eq.eq_next_main_date = datetime(dt.year, dt.month, dt.day)
    print(eq)
    eq.save()

    return render(request, 'PM/message.html', {'message': "save successful",
                                               'next': '/newequipment/'})


@login_required(login_url="/login/")
@permission_required('PM.add_maintenanceschedule', login_url='/login/')
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
                      {'message': "save successful",
                       'next': '/addmaintenance/'})
    else:
        tools = [i.tool_name for i in EquipmentTool.objects.all()]
        return render(request, 'PM/NewMaintenance.html',
                      {'toolnames': tools, })


@login_required(login_url="/login/")
@permission_required('PM.add_dailyreport', login_url='/login/')
def dailyReport(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/PM/dailyreport/')

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
                      {'message': "save successful",
                       'next': '/report/'})
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

            ord_tools_name=" -*- ".join(request.POST.getlist('ToolName')),
            ord_tools_qty=" -*- ".join(request.POST.getlist('ToolQty')),

        )

        od.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful",
                       'next': '/order/'})
    else:
        tools = [i.tool_name for i in EquipmentTool.objects.all()]
        ordNum = 'W' + datetime.now().strftime("%b%d%y%I%M") + \
            str(random.randint(0, 50))
        return render(request, 'PM/order.html',
                      {'toolnames': tools,
                       'ordNum': ordNum})


def viewMain(request, form_ID):
    if request.method != 'GET':
        data = request.POST
        print(data)
        ms = MaintenanceSchedule.objects.get(
            id=form_ID)

        tools = list(t for t in ms.ms_tools_name.split(
            ' -*- ') if t != '' and t != 'None')
        toolsNum = list(ms.ms_tools_qty.split(' -*- '))
        numbers = request.POST.getlist('toolback')

        if len(ms.maintenancecontent_set.all()) == 0 \
           or ms.maintenancecontent_set.all().last().mc_complete:
            mc = MaintenanceContent(
                mc_temp=ms,
                mc_content=" -*- ".join(request.POST.getlist('values')),
                mc_complete=True if request.POST.get('complete') else False
            )
        else:
            mc = ms.maintenancecontent_set.all().last()

        mc.mc_content = " -*- ".join(request.POST.getlist('values'))
        mc.mc_main_comment = data['materialsused']

        if not request.POST.get('complete'):
            mc.save()
            return HttpResponseRedirect('/viewTasks/')

        for i in range(len(tools)):
            to = EquipmentTool.objects.get(tool_name=tools[i])
            to.tool_quantity_left -= int(toolsNum[i]) - int(numbers[i])
            to.save()

        mc.mc_complete = True
        ms.ms_last_main_date = datetime.today()
        dt = datetime.today() + timedelta(ms.ms_maintenance_schedule * 7)
        ms.ms_next_main_date = datetime(dt.year, dt.month, dt.day)
        ms.save()

        return render(request, 'PM/message.html',
                      {'message': "submit successful",
                       'next': '/viewTasks/'})
    else:
        ms = get_object_or_404(MaintenanceSchedule, id=form_ID)
        lines = model_to_dict(ms)

        temp = [('schedule name', lines['ms_name']),
                ('serial number', lines['ms_serial_num']),
                ('internal part number', lines['ms_inter_part']), ]

        toolstemp = [(t for t in lines['ms_tools_name'].split(' -*- ') if t != '' and t != 'None'),
                     (t for t in lines['ms_tools_qty'].split(
                         ' -*- ') if t != 'None'),
                     ]
        toolstemp = list(zip(toolstemp[0], toolstemp[1]))

        labels = lines['ms_form_names'].split(' -*- ')
        labels = list(filter(lambda x: x != '' and x != ' -*-', labels))
        reqs = lines['ms_form_reqs'].split(' -*- ')
        types = lines['ms_form_fields'].split(' -*- ')

        if len(ms.maintenancecontent_set.all()) == 0:
            comment = ""
            values = ['' for i in range(len(labels))]
        elif not ms.maintenancecontent_set.all().last().mc_complete:
            comment = ms.maintenancecontent_set.all().last().mc_main_comment
            values = ms.maintenancecontent_set.all().last().mc_content\
                                                           .split(' -*- ')
        else:
            comment = ""
            values = ['' for i in range(len(labels))]

        MT = [(labels[i], values[i], reqs[i], types[i])
              for i in range(len(labels))]
        print(MT)
        return render(request, 'PM/Maintenance.html',
                      {'MT': MT,
                       'form_ID': form_ID,
                       'toolstemp': toolstemp,
                       'mainName': lines['ms_name'],
                       'temp': temp,
                       'materialsused': comment})


def viewTasks(request):
    if request.method == 'GET':
        resultList = taskLeft('today', request)
        resultList2 = taskLeft('whatever', request)
        return render(request, 'PM/viewForm.html',
                      {'titles': ["Name", "Type", "Add Date", 'Due Date', 'View'],
                       'content': resultList + resultList2})


def viewOrders(request, orderNumber):
    if request.method == 'GET':
        print(request.path)
        od = Order.objects.get(id=orderNumber)
        checkMark = ""
        if od.ord_complete:
            checkMark = "checked"

        toolstemp = [(t for t in od.ord_tools_name.split(' -*- ') if t != '' and t != 'None'),
                     (od.ord_tools_qty.split(' -*- ')),
                     ]

        toolstemp = list(zip(toolstemp[0], toolstemp[1]))
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
                       'toolstemp': toolstemp,
                       })
    else:
        print(request.POST)
        od = Order.objects.get(id=orderNumber)

        tools = list(t for t in od.ord_tools_name.split(
            ' -*- ') if t != '' and t != 'None')
        toolsNum = list(od.ord_tools_qty.split(' -*- '))
        numbers = request.POST.getlist('toolback')

        od.ord_comments = request.POST['materialsused']

        if not request.POST.get('complete'):
            od.ord_complete = False
            od.save()
            return HttpResponseRedirect('/viewTasks/')

        for i in range(len(tools)):
            to = EquipmentTool.objects.get(tool_name=tools[i])
            to.tool_quantity_left -= int(toolsNum[i]) - int(numbers[i])
            to.save()

        od.ord_complete = True
        od.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful",
                       'next': '/viewTasks/'})


def viewEq(request, eqNumber):
    if request.method == 'GET':
        eq = Equipment.objects.get(id=eqNumber)

        toolstemp = [(t for t in eq.eq_tools_name.split(' -*- ') if t != '' and t != 'None'),
                     (t for t in eq.eq_tools_qty.split(
                         ' -*- ') if t != '' and t != 'None'),
                     ]

        toolstemp = list(zip(toolstemp[0], toolstemp[1]))

        content = {'eqNumber': eqNumber,
                   'name': eq.eq_name,
                   'serial_num': eq.eq_serial_num,
                   'type': eq.eq_type,
                   'warranty': eq.eq_expir_date,
                   'purchase': eq.eq_purchase_date,
                   'manufacturer': eq.eq_manufacturer,
                   'internal_part_num': eq.eq_internal_part_num,
                   'schedule': eq.eq_maintenance_schedule,
                   'note': eq.eq_contact_notes,
                   'toolstemp': toolstemp,
                   'materialsused': eq.eq_main_comment,
                   }

        return render(request, 'PM/viewEquipment.html',
                      content)
    else:
        eq = Equipment.objects.get(id=eqNumber)
        print(request.POST)
        if not request.POST.get('complete'):
            eq.eq_main_comment = request.POST['materialsused']
            eq.save()
            return HttpResponseRedirect('/viewTasks/')

        tools = list(t for t in eq.eq_tools_name.split(
            ' -*- ') if t != '' and t != 'None')
        toolsNum = list(eq.eq_tools_qty.split(' -*- '))
        numbers = request.POST.getlist('toolback')

        for i in range(len(tools)):
            to = EquipmentTool.objects.get(tool_name=tools[i])
            to.tool_quantity_left -= int(toolsNum[i]) - int(numbers[i])
            to.save()

        eq.eq_last_main_date = datetime.today()
        dt = datetime.today() + timedelta(eq.eq_maintenance_schedule * 7)
        eq.eq_next_main_date = datetime(dt.year, dt.month, dt.day)
        eq.eq_main_comment = ''
        eq.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful",
                       'next': '/viewTasks/'})
