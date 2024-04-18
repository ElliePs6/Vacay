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
     path('show-employee/<int:employee_id>/', views.show_employee, name='show_employee'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('calendar/', views.calendar, name='calendar'),
    path('all_requests/', views.all_requests, name='all_requests'),
    path('add_request/',views.add_request,name='add_request'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('update/', views.update, name='update'),
    path('self-requests/',views.self_requests,name="self-requests"),
    path('list-all-requests/',views.list_all_requests,name='list_all_requests'),
    
    path('employee_navbar/', views.employee_navbar,name="employee_navbar"),
   # path('error_template/', views.error_template,name="error_template")



    
 
]