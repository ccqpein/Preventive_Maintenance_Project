from django.db import models


from django.contrib.auth.models import AbstractUser
# Create your models here.


class Equipment(models.Model):

    class Meta:
        permissions = (
            ("view_Equipment", "Can view equipments"),
        )

    eq_serial_num = models.CharField(max_length=100)
    eq_name = models.CharField(max_length=100)
    eq_type = models.CharField(max_length=100)
    eq_quantity_left = models.IntegerField(default=0)
    eq_expir_date = models.DateField()
    eq_purchase_date = models.DateField()
    eq_manufacturer = models.CharField(max_length=200)
    eq_internal_part_num = models.IntegerField(default=0)
    eq_maintenance_schedule = models.IntegerField(default=0)  # number of week
    eq_contact_notes = models.CharField(max_length=100)


class EquipmentTool(models.Model):
    tool_name = models.CharField(max_length=100)
    tool_type = models.CharField(max_length=100)
    tool_quantity_left = models.IntegerField(default=0)


class MaintenanceSchedule(models.Model):
    ms_serial_num = models.ForeignKey(Equipment)
    ms_inter_part = models.IntegerField(default=0)
    ms_tools = models.ManyToManyField(EquipmentTool)


class DailyReport(models.Model):

    class Meta:
        permissions = (
            ("view_DailyReport", "Can view daily report"),
        )

    dp_name = models.CharField(max_length=50)
    dp_shift = models.CharField(max_length=50)
    dp_date = models.DateField()
    dp_work_performed = models.CharField(max_length=1000)
    dp_problems_ident = models.CharField(max_length=1000)


class Order(models.Model):

    class Meta:
        permissions = (
            ("view_order", "Can view orders"),
        )

    ord_date = models.DateField()
    ord_req_by = models.CharField(max_length=50)
    ord_building = models.CharField(max_length=100)
    ord_floor = models.CharField(max_length=50)
    ord_room = models.CharField(max_length=50)
    ord_supervisor = models.CharField(max_length=100)
    ord_work_req = models.CharField(max_length=1000)
    ord_work_ord = models.CharField(max_length=50)
    ord_date_issue = models.DateField()
    ord_employee = models.CharField(max_length=100)
    ord_date_comp = models.DateField()
    ord_comments = models.CharField(max_length=1000)


class CheckList(models.Model):

    class Meta:
        permissions = (
            ("view_CheckList", "Can view CheckList"),
        )

    cl_plate_rating = models.CharField(max_length=100)
    cl_date = models.DateField()
    cl_operator = models.CharField(max_length=100)

    cl_start_time = models.CharField(max_length=100)
    cl_stop_time = models.CharField(max_length=100)
    cl_cool_time = models.CharField(max_length=100)

    cl_oil_level = models.CharField(max_length=100)
    cl_oil_add = models.CharField(max_length=100)

    cl_radiator_level = models.CharField(max_length=100)
    cl_radiator_add = models.CharField(max_length=100)

    cl_battery_level = models.CharField(max_length=100)
    cl_battery_charger = models.CharField(max_length=100)

    cl_oil_pressure = models.CharField(max_length=100)
    cl_fuel_tank = models.CharField(max_length=100)
    cl_engine_temp = models.CharField(max_length=100)
    cl_block_heater = models.CharField(max_length=100)
    cl_indicator_panel_light = models.CharField(max_length=100)

    cl_amp_1 = models.CharField(max_length=100)
    cl_amp_2 = models.CharField(max_length=100)
    cl_amp_3 = models.CharField(max_length=100)

    cl_eptsw = models.CharField(max_length=100)
    cl_cirnapmpbg = models.CharField(max_length=100)
    cl_grbblw = models.CharField(max_length=100)

    cl_fire_dampers2 = models.CharField(max_length=150)
    cl_fire_dampers3 = models.CharField(max_length=150)
    cl_fire_dampers4 = models.CharField(max_length=150)

    cl_checkbox = models.CharField(max_length=100)


class SafetyCheck(models.Model):

    class Meta:
        permissions = (
            ("view_SafetyCheck", "Can view safety check"),
        )

    sc_location = models.CharField(max_length=50)
    sc_desc = models.CharField(max_length=100)
    sc_brand_name = models.CharField(max_length=50)
    sc_inspection_date = models.DateField()
    sc_inspection_by = models.CharField(max_length=50)
    sc_next_inspection_date = models.DateField()
    sc_condition = models.CharField(max_length=50)
    sc_comment = models.CharField(max_length=200)
    sc_date = models.DateField()


class MyUser(AbstractUser):
    phone = models.CharField(max_length=20)
    note = models.CharField(max_length=500)
