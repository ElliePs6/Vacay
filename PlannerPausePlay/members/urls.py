from django.urls import path
from  .import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('company_home',views.company_home,name="company_home"),
    path('employee_home',views.employee_home,name="employee_home"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user',views.register_user,name="register_user"),
    path('user_view',views.user_view,name="user_view"),





    
]