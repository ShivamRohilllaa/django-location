from django.contrib import admin
from .models import Customer
from django.contrib.gis.admin import OSMGeoAdmin


@admin.register(Customer)
class CustomerAdmin(OSMGeoAdmin):
    list_display = ['id', 'name', 'user', 'location', 'longitude', 'latitude']
    search_fields = ['name', 'user__username']
