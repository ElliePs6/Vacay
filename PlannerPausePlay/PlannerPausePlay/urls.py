from django.contrib import admin
from django.urls import path, include
from members import views as members_views  # Assuming your view for admin_home is in members/views.py


urlpatterns = [
 path('admin/', admin.site.urls),
 path('', members_views.first_home, name='first_home'),  # Set admin_home as the landing page
 path('members',include('django.contrib.auth.urls')),
 path('members/',include('members.urls')),
 path('vacayvue/', include('VacayVue.urls')),  # Include other URLs from vacayvue app

]