from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

# Create your views here.
# from django.contrib.auth.models import User
from .models import Equipment, CheckList, DailyReport, Order, SafetyCheck, MyUser, MaintenanceContent, MaintenanceSchedule
from .forms import RegisterFrom
from datetime import datetime, timedelta


def taskLeft():
    resultList = []
    od = Order.objects.filter(ord_complete=False)
    for c in od:
        resultList.append(
            ("Work Order", c.ord_date, "\\"))

    eq = Equipment.objects.filter(
        eq_last_main_date=(datetime.today() - timedelta(days=7)))
    for c in eq:
        resultList.append(("Equipment", datetime.today(),
                           "\\"))

    mainT = MaintenanceContent.objects.filter(
        mc_last_main_date=(datetime.today() - timedelta(days=7)))
    for c in mainT:
        resultList.append(("Maintenance", datetime.today(),
                           "\\"))

    return resultList


@login_required(login_url="/login/")
def index(request):
    orderLeft = Order.objects.filter(ord_complete=False).count()
    tasks = taskLeft()
    return render(request, 'PM/index.html',
                  {'order_left': orderLeft,
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
        eq_manufacturer=data['manufacturer_date'],
        eq_internal_part_num=data['internal_part_num'],
        eq_contact_notes=data['note'],
        eq_maintenance_schedule=data['schedule'],
    )
    eq.save()

    return render(request, 'PM/message.html', {'message': "save successful"})


@login_required(login_url="/login/")
@permission_required('PM.view_Equipment', login_url='/login/')
def addMaintenance(request):
    if request.method != 'GET':
        data = request.POST
        mt = MaintenanceSchedule(
            ms_name=data['name'],
            ms_serial_num=data['serial_num'],
            ms_inter_part=data['internal_part_num'],

            ms_tools_name=" -*- ".join(request.POST.getlist('ToolName')),
            ms_tools_qty=" -*- ".join(request.POST.getlist('ToolQty')),
            ms_cons_name=" -*- ".join(request.POST.getlist('ConsumName')),
            ms_cons_qty=" -*- ".join(request.POST.getlist('ConsumQty')),

            ms_form_names=" -*- ".join(request.POST.getlist('mfname')),
            ms_form_reqs=" -*- ".join(request.POST.getlist('mfreq')),
            ms_form_fields=" -*- ".join(request.POST.getlist('mffieldtype')),
        )
        mt.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})
    else:
        return render(request, 'PM/NewMaintenance.html')


def viewMain(request, form_ID):
    if request.method != 'GET':
        data = request.POST
        print(data)
        mc = get_object_or_404(MaintenanceContent, id=form_ID)
        mc.mc_content = " -*- ".join(request.POST.getlist('values'))
        mc.save()
        return render(request, 'PM/message.html',
                      {'message': "submit successful"})
    else:
        tempID = get_object_or_404(MaintenanceContent, id=form_ID).mc_temp_id
        lines = model_to_dict(get_object_or_404(
            MaintenanceSchedule, id=tempID))
        print(lines)

        temp = [('ms_name', lines['ms_name']),
                ('serial number', lines['ms_serial_num']),
                ('internal part number', lines['ms_inter_part']),
                ('tools name', lines['ms_tools_name']),
                ('tools quantity', lines['ms_tools_name']),
                ]

        labels = lines['ms_form_names'].split(' -*- ')
        reqs = lines['ms_form_reqs'].split(' -*- ')
        types = lines['ms_form_fields'].split(' -*- ')
        MT = [(labels[i], reqs[i], types[i]) for i in range(len(labels))]

        return render(request, 'PM/Maintenance.html',
                      {'MT': MT,
                       'form_ID': form_ID,
                       'mainName': lines['ms_name'],
                       'temp': temp})


@login_required(login_url="/login/")
@permission_required('PM.add_checklist', login_url='/login/')
def checkList(request):
    if request.method != 'GET':
        data = request.POST
        cl = CheckList(
            cl_plate_rating=data['name_plate_rating'],
            cl_date=data['date'],
            cl_operator=data['operator'],

            cl_start_time=data['StartT'],
            cl_stop_time=data['StopT'],
            cl_cool_time=data['CoolDown'],

            cl_oil_level=data['OilLevel'],
            cl_oil_add=data['OilAdd'],

            cl_radiator_level=data['RadiatorL'],
            cl_radiator_add=data['RadiatorAdd'],

            cl_battery_level=data['BatteryL'],
            cl_battery_charger=data['BatteryCharger'],

            cl_oil_pressure=data['OilPressure'],
            cl_fuel_tank=data['FuelInTank'],
            cl_engine_temp=data['EngineTemp'],
            cl_block_heater=data['BlockHeater'],
            cl_indicator_panel_light=data['IndicatorPanelLight'],

            cl_amp_1=data['AMP1'],
            cl_amp_2=data['AMP2'],
            cl_amp_3=data['AMP3'],

            cl_eptsw=data['EPTSW'],
            cl_epilw=data['EPILW'],
            cl_fptsw=data['FPTSW'],
            cl_fpilw=data['FPILW'],
            cl_cirnapmpbg=data['CIRNAPMPBG'],
            cl_cirnapmpbgcomment=data['CIRNAPMPBGComment'],
            cl_grbblw=data['GRBBLW'],

            cl_fire_dampers2=data['FDO21'] + '/'
            + data['FDO22'] + '/' + data['FDO23'] + '/'
            + data['FDO24'] + '/' + data['FDO25'],
            cl_fire_dampers3=data['FDO31'] + '/'
            + data['FDO32'] + '/' + data['FDO33'] + '/'
            + data['FDO34'] + '/' + data['FDO35'],
            cl_fire_dampers4=data['FDO41'] + '/'
            + data['FDO42'] + '/' + data['FDO43'] + '/'
            + data['FDO44'] + '/' + data['FDO45'],

            cl_checkbox=data['checkbox'],

        )
        cl.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})
    else:
        return render(request, 'PM/CheckList.html')


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


@login_required(login_url="/login/")
@permission_required('PM.add_safetycheck', login_url='/login/')
def safetycheck(request):
    if request.method != 'GET':
        data = request.POST
        sc = SafetyCheck(
            sc_location=data['location'],
            sc_desc=data['descrip'],
            sc_brand_name=data['brandname'],
            sc_inspection_date=data['inspectiondate'],
            sc_inspection_by=data['inspectionby'],
            sc_next_inspection_date=data['nextinspectiondate'],
            sc_condition=data['condition'],
            sc_comment=data['comments'],
            sc_date=datetime.now().date(),
        )
        sc.save()
        return render(request, 'PM/message.html',
                      {'message': "save successful"})
    else:
        return render(request, 'PM/SafetyCheck.html')


def viewTasks(request):
    if request.method == 'GET':
        resultList = taskLeft()

        return render(request, 'PM/viewForm.html',
                      {'titles': ["Type", "Add Date", 'Due Date', 'View'],
                       'content': resultList})


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


def formTest(request):
    return render(request, 'PM/viewForm.html',
                  {'titles': [1, 2, 3, 4, 5],
                   'content': [(11, 22, 33, 44)]})
