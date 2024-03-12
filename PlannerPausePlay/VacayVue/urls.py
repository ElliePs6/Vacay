from django.urls import path
from  VacayVue import views

#url config
urlpatterns = [
    path('', views.home, name='home'),
   #s path('<int:year>/<str:month>/', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('list-requests/',views.list_requests,name="list-requests"),
    path('add-request/',views.add_request,name='add-request'),
    path('list-employees/',views.list_employees,name="list-employees"),
    
 
]