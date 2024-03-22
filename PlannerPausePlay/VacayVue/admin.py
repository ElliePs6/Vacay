from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employees, Companies, Requests, CustomUser
from  members.forms import RegisterCompanyForm
#Για να βλεπουμε τους πινακες στον admin
#admin.site.register(Employees)
#admin.site.register(Companies)
#admin.site.register(Requests)


admin.site.register(CustomUser,UserAdmin)




@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display=('username','join_date','email','user_type')
    ordering=('username',)
    search_fields=('username','email')

class CompaniesAdmin(admin.ModelAdmin):
    list_display=('companyname','email', 'hrname')  
    ordering=('companyname',)
    search_fields=('companyname','email')

    def add_view(self, request, form_url='', extra_context=None):
        self.form = RegisterCompanyForm  # Use the custom form for adding a new company
        return super().add_view(request, form_url, extra_context)

admin.site.register(Companies, CompaniesAdmin)

@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    fields=('EmployID',('StartDate','EndDate'),'Status','Type')
    list_display=('EmployID','StartDate','EndDate','Type','Status')
    search_fields=('Type','Status')
    list_filter=('StartDate','EndDate','Status')
