from rest_framework_gis.serializers import  GeoFeatureModelSerializer
from mobiletrans.mtlocation.models import (CTARailLines, 
            CityBorder, Neighborhood, Location, Landmark,
            TransitStop, Library, Hospital, PoliceStation, 
            )


class CTARailLinesSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = CTARailLines
        geo_field = "line"
        id_field = "objectid"
        fields = ('objectid', 'segment_id', 'asset_id', 'transit_lines',
                  'description', 'type', 'legend', 'alt_legend', 'branch',
                  'shape_len', 'line',
                  )
        

class CityBorderSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = CityBorder
        geo_field = "area"
        id_field = "objectid"
        fields = ('objectid', 'name', 'shape_area', 'shape_len', 'area' )


class NeighborhoodSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Neighborhood
        geo_field = "area"
        id_field = "slug"
        fields = ('created', 'modified', 'active', 'name', 'slug',
                  'area', 'uuid', 'long_name' )




class LandmarkSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Landmark
        geo_field = 'point'
        id_field = 'slug'
        fields = ('created', 'modified', 'active', 
                  'name', 'slug', 'uuid',
                  'address', 'architect', 'build_date',
                  'landmark_date',
                  )


class TransitStopSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = TransitStop
        geo_field = 'point'
        id_field = 'slug'
        fields = ('created', 'modified', 'active', 
                  'name', 'slug', 'uuid',
                  'route', 'stop_id', 'stop_code',
                  'description', 'url', 'location_type',
                  )
        

class LibrarySerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Library
        geo_field = 'point'
        id_field = 'slug'
        fields = ('created', 'modified', 'active', 
                  'name', 'slug', 'uuid',
                  'address', 'zip', 'hours',
                  'phone', 'website',
                  )
        

class HospitalSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Hospital
        geo_field = 'point'
        id_field = 'slug'
        fields = ('created', 'modified', 'active', 
                  'name', 'slug', 'uuid',
                  )
        

class PoliceStationSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = PoliceStation
        geo_field = 'point'
        id_field = 'slug'
        fields = ('created', 'modified', 'active', 
                  'name', 'slug', 'uuid',
                  'district', 'address', 'zip', 'website',
                  )


class LocationSerializer(GeoFeatureModelSerializer):

    def to_native(self, obj):
        obj = obj.as_leaf_class()
        if isinstance(obj, TransitStop):
           return TransitStopSerializer(obj).to_native(obj)
        elif isinstance(obj, Library):
            return LibrarySerializer(obj).to_native(obj)
        elif isinstance(obj, Landmark):
            return LandmarkSerializer(obj).to_native(obj)
        elif isinstance(obj, Hospital):
            return HospitalSerializer(obj).to_native(obj)
        elif isinstance(obj, PoliceStation):
            return PoliceStationSerializer(obj).to_native(obj)
        return super(LocationSerializer, self).to_native(obj)

    class Meta:
        model = Location
        geo_field = 'point'
        id_field = 'slug'
        fields = ('created', 'modified', 'active', 'name', 'slug', 
                  'uuid',
                  )