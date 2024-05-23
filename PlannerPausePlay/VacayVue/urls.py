from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('main_home/', views.main_home, name='main_home'),
    path('login/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
   
   


    path('employee_home/',views.employee_home,name="employee_home"),
    path('my_requests/',views.my_requests,name="my_requests"),
    path('delete_pending_request/<int:request_id>/', views.delete_pending_request, name='delete_pending_request'),
    path('add_employee/', views.add_employee, name="add_employee"),
      
    path('list_employees/',views.list_employees,name="list_employees"),
    path('show-employee/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('edit-employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('company_home/', views.company_home, name='company_home'),
    path('add_request/',views.add_request,name='add_request'),

    path('list_requests/',views.list_all_requests,name='list_all_requests'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
   path('approve_leave_request/<int:request_id>/', views.handle_leave_request, {'action': 'approve'}, name='approve_leave_request'),
    path('request_details/<int:request_id>/', views.request_details, name='request_details'),

    path('update_default_days/<int:leave_type_id>/', views.update_default_days, name='update_default_days'),
    path('manage_leave_type/', views.manage_leave_type, name='manage_leave_type'),
    path('balance-data/', views.balance_data, name='balance_data'),
    path('get_target_month/', views.get_target_month, name='get_target_month'),
  
    #path('change-password/', views.change_password, name='change_password'),

    path('calendar/', views.calendar, name='calendar'),
    path('all_requests/', views.all_requests, name='all_requests'),
    
    
   
   # path('error_template/', views.error_template,name="error_template")



    
 
]