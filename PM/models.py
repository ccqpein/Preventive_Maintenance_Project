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


class MyUser(AbstractUser):
    phone = models.CharField(max_length=20)
    note = models.CharField(max_length=500)
