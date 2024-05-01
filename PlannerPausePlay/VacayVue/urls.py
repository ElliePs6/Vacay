from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('main_home/', views.main_home, name='main_home'),
    path('login/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
   
   


    path('employee_home/',views.employee_home,name="employee_home"),
    path('self-requests/',views.self_requests,name="self-requests"),
    path('register_employee/', views.register_employee, name="register_employee"),
      
    path('list-employees/',views.list_employees,name="list-employees"),
    path('show-employee/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('company_home/', views.company_home, name='company_home'),
    path('add_request/',views.add_request,name='add_request'),

    path('list-all-requests/',views.list_all_requests,name='list_all_requests'),
    path('approve_leave_request/<int:request_id>/', views.approve_leave_request, name='approve_leave_request'),
    path('reject-leave-request/<int:request_id>/', views.reject_leave_request, name='reject_leave_request'),
    path('request_details/<int:request_id>/', views.request_details, name='request_details'),

    #path('balance/', views.balance, name='balance'),
    path('update_default_days/<int:leave_type_id>/', views.update_default_days, name='update_default_days'),
    #path('manage_leave_balance/', views.manage_leave_balance, name='manage_leave_balance'),
    path('manage_leave_type/', views.manage_leave_type, name='manage_leave_type'),
  

    path('calendar/', views.calendar, name='calendar'),
    path('all_requests/', views.all_requests, name='all_requests'),
    
    
   
   # path('error_template/', views.error_template,name="error_template")



    
 
]