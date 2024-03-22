from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employees, Companies, Requests, CustomUser
from members.forms import RegisterCompanyForm


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('companyname', 'hrname')
    ordering = ('companyname',)
    search_fields = ('companyname', 'hrname')

    def add_view(self, request, form_url='', extra_context=None):
        self.form = RegisterCompanyForm
        return super().add_view(request, form_url, extra_context)


class CustomUserAdmin(UserAdmin):
    list_display = ('user_type', 'company')


admin.site.register(CustomUser, CustomUserAdmin)
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
