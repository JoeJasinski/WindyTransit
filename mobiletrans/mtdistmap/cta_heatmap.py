import os
import mapnik
from django.conf import settings
subquery1 = """(SELECT * FROM   public.mtlocation_region,  public.mtlocation_neighborhood,  public.django_content_type WHERE 
  mtlocation_region.id = mtlocation_neighborhood.region_ptr_id AND
  mtlocation_region.content_type_id = django_content_type.id) as foo"""

subquery2 = """(SELECT * FROM 
  mtlocation_location as loc
  inner join django_content_type as ct on (loc.content_type_id = ct.id)
  left outer join public.mtlocation_gplace as place on  ( loc.id = place.location_ptr_id )
where ct.model not in ('transitstop')) as foo"""

subquery3 = """(SELECT 
  l.id,   l.created,    l.modified,   l.active,   l.name, 
  s.location_type,  s.url,  s.description,   s.stop_code,  s.stop_id,  s.location_ptr_id, 
  l.slug,   l.uuid,   l.content_type_id,   l.point
FROM 
  mtlocation_location l, 
  mtlocation_transitstop s
WHERE 
  s.location_ptr_id = l.id
  and s.location_type = 1) as bar
"""

cta_heatmap_xml = os.path.join(settings.PROJECT_ROOT, 'mtdistmap', 'cta_heatmap.xml')
f = open(cta_heatmap_xml)
schema = f.read()
f.close()

m = mapnik.Map(600,600)
mapnik.load_map_from_string(m, schema)
ds = mapnik.PostGIS(dbname='mobiletrans', user='mobiletrans', host='localhost', password='1234', table='mtlocation_cityborder')
m.layers[0].datasource = ds
ds = mapnik.PostGIS(dbname='mobiletrans', user='mobiletrans', host='localhost', password='1234', table=subquery1, geometry_table="mtlocation_region", geometry_field='area')
m.layers[1].datasource = ds
ds = mapnik.PostGIS(dbname='mobiletrans', user='mobiletrans', host='localhost', password='1234', table=subquery2,  geometry_table="mtlocation_location", geometry_field='point')
m.layers[2].datasource = ds
ds = mapnik.PostGIS(dbname='mobiletrans', user='mobiletrans', host='localhost', password='1234', table='mtlocation_ctaraillines', )
m.layers[3].datasource = ds
ds = mapnik.PostGIS(dbname='mobiletrans', user='mobiletrans', host='localhost', password='1234', table=subquery3, geometry_table="mtlocation_location", geometry_field='point' )
m.layers[4].datasource = ds
m.zoom_all()
mapnik.render_to_file(m, 'chicago.png', 'png')
m.zoom(1)
mapnik.render_to_file(m, 'chicago2.png', 'png')