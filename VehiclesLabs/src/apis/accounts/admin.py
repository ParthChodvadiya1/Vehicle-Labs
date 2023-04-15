from django.contrib import admin
from .models import UserDetail, PhoneOTP

# Register your models here.

admin.site.register(UserDetail)
admin.site.register(PhoneOTP)
