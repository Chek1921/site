from django.contrib import admin
from .models import Report, Bill, CustomUser, New, District, Bill_name, Bill_rate
# Register your models here.

admin.site.register(Report)
admin.site.register(Bill)
admin.site.register(New)
admin.site.register(District)
admin.site.register(Bill_name)
admin.site.register(Bill_rate)
admin.site.register(CustomUser)