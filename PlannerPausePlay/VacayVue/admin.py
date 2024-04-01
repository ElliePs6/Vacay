from django.contrib import admin
from .models import Employee, Company, Requests, CustomUser





admin.site.register(CustomUser)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hr_name')
    ordering = ('name',)
    search_fields = ('name', 'hr_name')

admin.site.register(Company, CompanyAdmin)
    

@admin.register(Employee)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'join_date') 
    ordering = ('first_name',)


@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    fields = ('employeeID', ('StartDate', 'EndDate'), 'Status', 'Type')
    list_display = ('employeeID', 'StartDate', 'EndDate', 'Type', 'Status')
    search_fields = ('Type', 'Status')
    list_filter = ('StartDate', 'EndDate', 'Status')