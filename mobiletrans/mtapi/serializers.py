from rest_framework_gis.serializers import  GeoFeatureModelSerializer
from mobiletrans.mtlocation.models import CTARailLines


class CTARailLinesSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = CTARailLines
        geo_field = "line"
        id_field = "objectid"
        fields = ('objectid', 'segment_id', 'asset_id', 'transit_lines',
                  'description', 'type', 'legend', 'alt_legend', 'branch',
                  'shape_len', 'line',
                  )