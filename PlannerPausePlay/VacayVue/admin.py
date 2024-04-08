from django.contrib import admin
from .models import Employee, Company, Request, CustomUser





admin.site.register(CustomUser)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hr_name','afm', 'dou')
    ordering = ('afm',)
    search_fields = ('name', 'afm')

admin.site.register(Company, CompanyAdmin)
    

@admin.register(Employee)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'join_date') 
    ordering = ('first_name',)


@admin.register(Request)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'type','description')
    ordering = ('type',)
    