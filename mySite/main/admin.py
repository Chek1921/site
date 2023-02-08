from django.contrib import admin
from .models import Reports, Bill, CustomUser

# Register your models here.

admin.site.register(Reports)
admin.site.register(Bill)
admin.site.register(CustomUser)