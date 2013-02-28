from django.contrib.gis.gdal import DataSource
ds = DataSource('/home/jjasinski/Sites/windytransit/data/City_Boundary/City_Boundary.shp')
layer = ds[0]

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point
gcoord = SpatialReference(4326)
mycoord = SpatialReference(102671)
trans = CoordTransform(gcoord, mycoord)
object = layer[0]
object.geom.transform(trans)
