from django.contrib import admin
from . import models

class LandmarkAdmin(admin.ModelAdmin):
    
    list_display = ['uuid','name','point','address']

class LocationAdmin(admin.ModelAdmin):
    
    list_display = ['uuid','name','point',]

admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Landmark, LandmarkAdmin)