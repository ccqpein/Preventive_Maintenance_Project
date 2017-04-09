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
    eq_internal_part_num = models.CharField(max_length=100)
    eq_maintenance_schedule = models.IntegerField(default=1)  # number of week
    eq_contact_notes = models.CharField(max_length=100)

    eq_add_date = models.DateField(auto_now=True)
    eq_last_main_date = models.DateField(null=True)
    eq_next_main_date = models.DateField(null=True)


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
    ord_date_comp = models.DateField(null=True)
    ord_comments = models.CharField(max_length=1000)

    ord_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.ord_date.__str__()


class MyUser(AbstractUser):
    phone = models.CharField(max_length=20)
    note = models.CharField(max_length=500)
