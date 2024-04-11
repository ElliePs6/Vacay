from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('main_home/', views.main_home, name='main_home'),
    path('login/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
    path('company_home/', views.company_home, name='company_home'),  
    path('employee_home/',views.employee_home,name="employee_home"),
    path('register_employee/', views.register_employee, name="register_employee"),  
    path('list-employees/',views.list_employees,name="list-employees"),

    path('calendar/', views.calendar, name='calendar'),
    path('all_requests/', views.all_requests, name='all_requests'),
    path('add_request/',views.add_request,name='add_request'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),

     #path('get_request_details/<int:request_id>/', views.get_request_details, name='get_request_details'),
     #path('update_request/<int:request_id>/', views.update_request, name='update_request'),

    path('request-edit/<int:request_id>/', views.edit_request, name='request-edit'),
    path('list-requests/',views.list_requests,name="list-requests"),
    path('employee_navbar/', views.employee_navbar,name="employee_navbar"),
   # path('error_template/', views.error_template,name="error_template")



    
 
]