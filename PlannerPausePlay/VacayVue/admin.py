from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employees
from .models import Companies
from .models import Requests
from.models import CustomUser
#Για να βλεπουμε τους πινακες στον admin
#admin.site.register(Employees)
#admin.site.register(Companies)
#admin.site.register(Requests)


admin.site.register(CustomUser,UserAdmin)



admin.site.register(Employees)
'''
class EmployeesAdmin(admin.ModelAdmin):
    list_display=('Username','join_date','Email','Role')
    ordering=('Username',)
    search_fields=('Username','Email')
'''
admin.site.register(Companies)
'''
class CompaniesAdmin(admin.ModelAdmin):
    list_display=('Companyname','Email')
    ordering=('Companyname',)
    search_fields=('Companyname','Email')
'''
@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    fields=('EmployID',('StartDate','EndDate'),'Status','Type')
    list_display=('EmployID','StartDate','EndDate','Type','Status')
    search_fields=('Type','Status')
    list_filter=('StartDate','EndDate','Status')
