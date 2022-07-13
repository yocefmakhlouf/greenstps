from django.contrib import admin

from api.models import Data
from api.models import Refresh_token,compets,last_users

# Register your models here.
@admin.register(Data)
class RequestDemo(admin.ModelAdmin):
    list_display = [field.name for field in Data._meta.get_fields()]

@admin.register(Refresh_token)
class RequestDemo(admin.ModelAdmin):
    list_display = [field.name for field in Refresh_token._meta.get_fields()]
@admin.register(compets)
class RequestDemo(admin.ModelAdmin):
    list_display = [field.name for field in compets._meta.get_fields()]
@admin.register(last_users)
class RequestDemo(admin.ModelAdmin):
    list_display = [field.name for field in last_users._meta.get_fields()]