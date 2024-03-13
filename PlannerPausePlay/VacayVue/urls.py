from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('register/', views.register, name="register"),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('list-requests/',views.list_requests,name="list-requests"),
    path('add-request/',views.add_request,name='add-request'),
    path('list-employees/',views.list_employees,name="list-employees"),

    
 
]