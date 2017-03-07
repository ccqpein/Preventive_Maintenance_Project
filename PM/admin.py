from django.contrib import admin

# Register your models here.
from .models import Equipment, EquipmentTool, MyUser


admin.site.register(Equipment)
admin.site.register(EquipmentTool)
admin.site.register(MyUser)
