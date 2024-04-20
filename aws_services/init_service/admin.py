from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Role)
admin.site.register(AWSUser)
admin.site.register(AvailableScreens)
admin.site.register(UserScreens)
