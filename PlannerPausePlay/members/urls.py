from django.urls import path
from  .import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('company_home',views.company_home,name="company_home"),
    path('employee_home',views.employee_home,name="employee_home"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_company',views.register_company,name="register_company"),
    path('register_employee',views.register_employee,name="register_employee"),






    
]