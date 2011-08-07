from django.contrib.gis import admin
from . import models
from mtcore import app_renamer

app_renamer.AppLabelRenamer(native_app_label=u'mtlocation', app_label=u'Location').main()

class LocationAdmin(admin.GeoModelAdmin):
    
    list_display = ['uuid','name','point',]


class LandmarkAdmin(admin.GeoModelAdmin):
    
    list_display = LocationAdmin.list_display + ['address',]


class TransitStopAdmin(admin.GeoModelAdmin):
    
    filter_horizontal = ['route',]
    search_fields = ['stop_id','name']
    list_filter = ['location_type',]
    list_display = LocationAdmin.list_display  + ['stop_id','location_type']


class TransitRouteAdmin(admin.ModelAdmin):
    search_fields = ['name']    
    list_display = ['route_id','short_name','long_name','get_type_display',]


class LibraryAdmin(admin.GeoModelAdmin):
    
    list_display = LocationAdmin.list_display + ['address',]

admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Landmark, LandmarkAdmin)
admin.site.register(models.TransitRoute, TransitRouteAdmin)
admin.site.register(models.TransitStop, TransitStopAdmin)
admin.site.register(models.Library, LibraryAdmin)