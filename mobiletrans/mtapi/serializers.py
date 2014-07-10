from rest_framework_gis.serializers import  GeoFeatureModelSerializer
from mobiletrans.mtlocation.models import CTARailLines, CityBorder, Neighborhood


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

