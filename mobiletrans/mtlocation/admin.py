from django.contrib import admin
from . import models
from mtcore import app_renamer

app_renamer.AppLabelRenamer(native_app_label=u'mtlocation', app_label=u'Location').main()

class LocationAdmin(admin.ModelAdmin):
    
    list_display = ['uuid','name','point',]


class LandmarkAdmin(admin.ModelAdmin):
    
    list_display = ['uuid','name','point','address',]


class TransitStopAdmin(admin.ModelAdmin):
    list_filter = ['location_type',]
    list_display = ['stop_id','uuid','name','point','location_type']

admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Landmark, LandmarkAdmin)
admin.site.register(models.TransitStop, TransitStopAdmin)