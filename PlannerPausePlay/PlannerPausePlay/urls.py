from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from members import views as members_views


urlpatterns = [
 path('admin/', admin.site.urls),
 path('', members_views.admin_landpage, name='admin_landpage'),  #  admin_home as  landing page
 path('members',include('django.contrib.auth.urls')),
 path('members/',include('members.urls')),
 path('vacayvue/', include('VacayVue.urls')),  

]
# Serving static files during development
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)#