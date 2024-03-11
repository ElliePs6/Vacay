from django.urls import path
from .views import home,register,login_user,logout_user,list_requests,add_request,list_employees

#url config
urlpatterns = [
    path('', home, name='home'),
    path('<int:year>/<str:month>/', home, name='home'),
    path('register/', register, name="register"),
    path('login_user/', login_user, name="login_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('list-requests/',list_requests,name="list-requests"),
    path('add-request/',add_request,name='add-request'),
    path('list-employees/',list_employees,name="list-employees"),
]