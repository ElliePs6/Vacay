from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('main_home/', views.main_home, name='main_home'),
    path('login/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
    path('register_employee/<int:company_id>/', views.register_employee, name="register_employee"),  # Added company_id path with converter
    path('list-employees/',views.list_employees,name="list-employees"),
    path('company_home/<int:company_id>/', views.company_home, name='company_home'),
    path('employee_home/',views.employee_home,name="employee_home"),
    path('calendar/', views.calendar, name='calendar'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),    
    path('add-request/',views.add_request,name='add-request'),
    path('list-requests/',views.list_requests,name="list-requests"),
    path('employee_navbar/', views.employee_navbar,name="employee_navbar"),
   # path('error_template/', views.error_template,name="error_template")



    
 
]