from django.db import models


from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    phone = models.CharField(max_length=20)
    note = models.CharField(max_length=500)


class Equipment(models.Model):

    eq_serial_num = models.CharField(max_length=100)
    eq_name = models.CharField(max_length=100)
    eq_type = models.CharField(max_length=100)
    eq_quantity_left = models.IntegerField(default=0)
    eq_expir_date = models.DateField()
    eq_purchase_date = models.DateField()
    eq_manufacturer = models.CharField(max_length=200)
    eq_internal_part_num = models.CharField(max_length=100)
    eq_maintenance_schedule = models.IntegerField(default=1)  # number of week
    eq_contact_notes = models.CharField(max_length=100)

    eq_tools_name = models.CharField(max_length=500)
    eq_tools_qty = models.CharField(max_length=100)

    eq_add_date = models.DateField(auto_now=True)
    eq_last_main_date = models.DateField(null=True)
    eq_next_main_date = models.DateField(null=True)

    eq_main_comment = models.CharField(max_length=500, blank=True)


class EquipmentTool(models.Model):
    tool_name = models.CharField(max_length=100)
    tool_type = models.CharField(max_length=100)
    tool_quantity_left = models.IntegerField(default=0)


class MaintenanceSchedule(models.Model):
    ms_name = models.CharField(max_length=100)
    ms_date = models.DateField(auto_now=True)
    ms_serial_num = models.CharField(max_length=100)
    ms_inter_part = models.CharField(max_length=100)

    ms_tools_name = models.CharField(max_length=500)
    ms_tools_qty = models.CharField(max_length=100)

    ms_form_names = models.CharField(max_length=1000)
    ms_form_reqs = models.CharField(max_length=100)
    ms_form_fields = models.CharField(max_length=200)
    ms_maintenance_schedule = models.IntegerField(default=1)  # number of week

    ms_last_main_date = models.DateField(null=True)
    ms_next_main_date = models.DateField(null=True)


class MaintenanceContent(models.Model):
    mc_temp = models.ForeignKey(MaintenanceSchedule)
    mc_content = models.CharField(max_length=2000)
    mc_date = models.DateField(auto_now=True)

    mc_main_comment = models.CharField(max_length=500)
    mc_complete = models.BooleanField(default=False)


class DailyReport(models.Model):

    dp_name = models.CharField(max_length=50)
    dp_shift = models.CharField(max_length=50)
    dp_date = models.DateField()
    dp_work_performed = models.CharField(max_length=1000)
    dp_problems_ident = models.CharField(max_length=1000)

    dp_user = models.ForeignKey(MyUser)


class Order(models.Model):

    ord_serial_num = models.CharField(max_length=100)

    ord_date = models.DateField(auto_now=True)
    ord_req_by = models.CharField(max_length=50)
    ord_building = models.CharField(max_length=100)
    ord_floor = models.CharField(max_length=50)
    ord_room = models.CharField(max_length=50)
    ord_supervisor = models.CharField(max_length=100)
    ord_work_req = models.CharField(max_length=1000)
    ord_work_ord = models.CharField(max_length=50)
    ord_date_issue = models.DateField()
    ord_employee = models.CharField(max_length=100)
    ord_date_comp = models.DateField(null=True, blank=True)
    ord_comments = models.CharField(max_length=1000)

    ord_tools_name = models.CharField(max_length=500)
    ord_tools_qty = models.CharField(max_length=500)

    ord_assign = models.ForeignKey(MyUser, null=True, blank=True)

    ord_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.ord_date.__str__()
