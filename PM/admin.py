from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Register your models here.
from .models import Equipment, CheckList, DailyReport, Order, SafetyCheck, MyUser, MaintenanceSchedule, MaintenanceContent


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
    list_display = ('ord_date', 'ord_req_by')

admin.site.register(Equipment)
admin.site.register(DailyReport)
admin.site.register(Order, OrderAdmin)
admin.site.register(CheckList)
admin.site.register(SafetyCheck)
admin.site.register(MaintenanceSchedule)
admin.site.register(MaintenanceContent)
admin.site.register(MyUser, CustomUserAdmin)
