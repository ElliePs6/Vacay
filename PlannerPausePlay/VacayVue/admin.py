from django.contrib import admin
from .models import Employees
from .models import Companies
from .models import Requests
#Για να βλεπουμε τους πινακες στον admin
admin.site.register(Employees)
admin.site.register(Companies)
admin.site.register(Requests)