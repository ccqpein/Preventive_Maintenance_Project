from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Permission

# Register your models here.
from .models import Equipment, EquipmentTool, DailyReport, Order, MyUser, MaintenanceSchedule, MaintenanceContent


class User_exAdmin(admin.ModelAdmin):
    list_display = ('valid_code', 'valid_time', 'email')  # need finish


class CustomUserAdmin(UserAdmin):

    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'email',
                             'is_active', 'is_staff', 'is_superuser')
        self.search_fields = ('username', 'email', 'phone')
        self.form = UserChangeForm
        self.add_form = UserCreationForm

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
                              (_('Personal info'), {
                                  'fields': ('email', 'phone')}),
                              (_('Permissions'), {
                                  'fields': ('is_active', 'is_staff', 'groups')}),
                              (_('Important dates'), {
                                  'fields': ('last_login', 'date_joined')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'phone', 'password1', 'password2', 'email', 'is_active', 'is_staff', 'groups'),
                                          }),
                                  )
        else:
            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
                              (_('Personal info'), {
                               'fields': ('phone', 'email')}),
                              (_('Permissions'), {
                               'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                              (_('Important dates'), {
                                  'fields': ('last_login', 'date_joined')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'phone', 'password1', 'password2', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
                                  )
        return super(CustomUserAdmin, self).changelist_view(request, extra_context)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('ord_date', 'ord_date_issue', 'ord_req_by')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('eq_name', 'eq_last_main_date', 'eq_next_main_date')


class EquipmentToolAdmin(admin.ModelAdmin):
    list_display = ('tool_name', 'tool_quantity_left')


class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('ms_name', 'ms_last_main_date', 'ms_next_main_date')


class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('dp_name', 'dp_date')


class MaintenanceContentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'mc_date')

    def get_name(self, mo):
        return mo.mc_temp.ms_name


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentTool, EquipmentToolAdmin)
admin.site.register(DailyReport, DailyReportAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MaintenanceSchedule, MaintenanceScheduleAdmin)
admin.site.register(MaintenanceContent, MaintenanceContentAdmin)
admin.site.register(MyUser, CustomUserAdmin)
# admin.site.register(Permission)
