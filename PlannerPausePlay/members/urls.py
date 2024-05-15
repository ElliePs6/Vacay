from django.urls import path
from  .import views

urlpatterns = [
    path('',views.admin_landpage,name="admin_landpage"),
    path('admin_home/',views.admin_home,name="admin_home"),
    path('logout_admin/', views.logout_admin, name="logout_admin"),
    path('register_company/',views.register_company,name="register_company"),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('switch_to_company_login/', views.switch_to_company_login, name='switch_to_company_login'),
]