from django.contrib.gis import admin
from . import models
from mtcore import app_renamer

app_renamer.AppLabelRenamer(native_app_label=u'mtlocation', app_label=u'Location').main()

class LocationAdmin(admin.GeoModelAdmin):
    
    list_display = ['uuid','name','point',]


class LandmarkAdmin(admin.GeoModelAdmin):
    
    list_display = ['uuid','name','point','address',]


class TransitStopAdmin(admin.GeoModelAdmin):
    list_filter = ['location_type',]
    list_display = ['stop_id','uuid','name','point','location_type']


class TransitRouteAdmin(admin.ModelAdmin):
    
    list_display = ['route_id','short_name','long_name','get_type_display',]


admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Landmark, LandmarkAdmin)
admin.site.register(models.TransitRoute, TransitRouteAdmin)
admin.site.register(models.TransitStop, TransitStopAdmin)