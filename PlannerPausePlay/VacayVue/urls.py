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
    

    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'), 
    path('list-requests/',views.list_requests,name="list-requests"),
    path('employee_navbar/', views.employee_navbar,name="employee_navbar"),
   # path('error_template/', views.error_template,name="error_template")



    
 
]