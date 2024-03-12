from django.contrib import admin
from .models import Employees
from .models import Companies
from .models import Requests
#Για να βλεπουμε τους πινακες στον admin
#admin.site.register(Employees)
#admin.site.register(Companies)
#admin.site.register(Requests)

@admin.register(Employees)

class EmployeesAdmin(admin.ModelAdmin):
    list_display=('Firstname','Lastname','Email','Role')
    ordering=('Username',)
    search_fields=('Username','Email')

@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display=('Companyname','Email')
    ordering=('Companyname',)
    search_fields=('Companyname','Email')

@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    fields=('EmployID',('StartDate','EndDate'),'Status','Type')
    list_display=('EmployID','StartDate','EndDate','Type','Status')
    search_fields=('Type','Status')
    list_filter=('StartDate','EndDate','Status')
