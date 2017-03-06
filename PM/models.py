from django.db import models

# Create your models here.


class Equipment(models.Model):

    class Meta:
        permissions = (
            ("view_Equipment", "Can view equipments"),
        )

    serial_num = models.CharField(max_length=100)
    eq_name = models.CharField(max_length=100)
    eq_type = models.CharField(max_length=100)
    quantity_left = models.IntegerField(default=0)


class Equipment_tool(models.Model):
    tool_name = models.CharField(max_length=100)
    tool_type = models.CharField(max_length=100)
