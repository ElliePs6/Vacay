from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('main_home/', views.main_home, name='main_home'),
    path('login/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
   
   


    path('employee_home/',views.employee_home,name="employee_home"),

     path('register_employee/', views.register_employee, name="register_employee"),  
    path('list-employees/',views.list_employees,name="list-employees"),
    path('show-employee/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('company_home/', views.company_home, name='company_home'),
    path('approve-request/', views.approve_request, name='approve_request'),
    path('reject-request/', views.reject_request, name='reject_request'),

    path('calendar/', views.calendar, name='calendar'),
    path('all_requests/', views.all_requests, name='all_requests'),
    path('add_request/',views.add_request,name='add_request'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('update/', views.update, name='update'),
    path('self-requests/',views.self_requests,name="self-requests"),
    path('list-all-requests/',views.list_all_requests,name='list_all_requests'),
    
    #path('dashboard/', views.dashboard,name="dashboard"),
   # path('error_template/', views.error_template,name="error_template")



    
 
]