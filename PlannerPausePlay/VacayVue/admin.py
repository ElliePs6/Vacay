from django.contrib import admin
from .models import Employee, Company, Requests, CustomUser, Admins


@admin.register(Admins)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    ordering = ('user__username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'


admin.site.register(CustomUser)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hr_name')
    ordering = ('name',)
    search_fields = ('name', 'hr_name')

admin.site.register(Company, CompanyAdmin)
    

@admin.register(Employee)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','company', 'join_date') 
    ordering = ('company',)


@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    fields = ('EmployID', ('StartDate', 'EndDate'), 'Status', 'Type')
    list_display = ('EmployID', 'StartDate', 'EndDate', 'Type', 'Status')
    search_fields = ('Type', 'Status')
    list_filter = ('StartDate', 'EndDate', 'Status')