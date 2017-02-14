from django.db import models

# Create your models here.


class Equipment(models.Model):
    serial_num = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    quantity_left = models.IntegerField(default=0)
