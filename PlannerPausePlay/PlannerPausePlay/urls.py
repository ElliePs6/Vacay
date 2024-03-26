from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from members import views as members_views  # Assuming your view for admin_home is in members/views.py


urlpatterns = [
 path('admin/', admin.site.urls),
 path('', members_views.admin_landpage, name='admin_landpage'),  # Set admin_home as the landing page
 path('members',include('django.contrib.auth.urls')),
 path('members/',include('members.urls')),
 path('vacayvue/', include('VacayVue.urls')),  # Include other URLs from vacayvue app

]
# Serving static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)