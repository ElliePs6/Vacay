from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employees, Companies, Requests, CustomUser, Admins
from members.forms import RegisterCompanyForm, AdminUserCreationForm, AdminUserChangeForm


@admin.register(Admins)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    ordering = ('user__username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'


admin.site.register(CustomUser)


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('companyname', 'hrname')
    ordering = ('companyname',)
    search_fields = ('companyname', 'hrname')

admin.site.register(Companies, CompaniesAdmin)
    

@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('username', 'join_date')  # Removed 'employe_email'
    ordering = ('username',)


@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    fields = ('EmployID', ('StartDate', 'EndDate'), 'Status', 'Type')
    list_display = ('EmployID', 'StartDate', 'EndDate', 'Type', 'Status')
    search_fields = ('Type', 'Status')
    list_filter = ('StartDate', 'EndDate', 'Status')