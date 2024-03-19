from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),    
    path('list-requests/',views.list_requests,name="list-requests"),
    path('add-request/',views.add_request,name='add-request'),
    path('list-employees/',views.list_employees,name="list-employees"),
    path('employee_navbar/', views.employee_navbar,name="employee_navbar"),
    path('navbar_company/', views.navbar_company,name="navbar_company")


    
 
]