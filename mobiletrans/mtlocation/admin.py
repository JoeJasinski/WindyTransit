from django.contrib.gis import admin
from . import models
from mobiletrans.mtcore import app_renamer

app_renamer.AppLabelRenamer(native_app_label=u'mtlocation', app_label=u'Location').main()

class LocationAdmin(admin.GeoModelAdmin):
    
    search_fields = ['name','uuid']
    list_display = ['uuid','name','point',]
    readonly_fields = ['uuid','slug','created','modified']


class LandmarkAdmin(admin.GeoModelAdmin):
    
    search_fields = LocationAdmin.search_fields + ['address']
    list_display = LocationAdmin.list_display + ['address',]
    readonly_fields = LocationAdmin.readonly_fields


class TransitStopAdmin(admin.GeoModelAdmin):
    
    filter_horizontal = ['route',]
    search_fields = LocationAdmin.search_fields + ['stop_id',]
    list_filter = ['location_type',]
    list_display = LocationAdmin.list_display  + ['stop_id','location_type']
    readonly_fields = LocationAdmin.readonly_fields


class TransitRouteAdmin(admin.ModelAdmin):
    search_fields = ['name']   
    readonly_fields = ['uuid'] 
    list_display = ['route_id','short_name','long_name','get_type_display',]


class LibraryAdmin(admin.GeoModelAdmin):

    search_fields = LocationAdmin.search_fields + ['address','zip']  
    list_display = LocationAdmin.list_display + ['address',]
    readonly_fields = LocationAdmin.readonly_fields

class HospitalAdmin(admin.GeoModelAdmin):

    search_fields = LocationAdmin.search_fields
    list_display = LocationAdmin.list_display 
    readonly_fields = LocationAdmin.readonly_fields


class RegionAdmin(admin.GeoModelAdmin):

    search_fields = ['name','uuid'] 
    list_display = ['uuid','name']
    

class NeighborhoodAdmin(admin.GeoModelAdmin):

    search_fields = RegionAdmin.search_fields + ['long_name',]
    list_display = RegionAdmin.list_display + ['long_name',]

class ZipcodeAdmin(admin.GeoModelAdmin):

    search_fields = RegionAdmin.search_fields
    list_display = RegionAdmin.list_display

class GPlaceAdmin(admin.GeoModelAdmin):

    search_fields = LocationAdmin.search_fields
    list_display = LocationAdmin.list_display 
    readonly_fields = LocationAdmin.readonly_fields



admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Landmark, LandmarkAdmin)
admin.site.register(models.TransitRoute, TransitRouteAdmin)
admin.site.register(models.TransitStop, TransitStopAdmin)
admin.site.register(models.Library, LibraryAdmin)
admin.site.register(models.Hospital, HospitalAdmin)
admin.site.register(models.GPlace, GPlaceAdmin)

admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Neighborhood, NeighborhoodAdmin)
admin.site.register(models.Zipcode, ZipcodeAdmin)
