import os
import mapnik
from django.conf import settings


DB_NAME = settings.DATABASES['default']['NAME']
DB_USER = settings.DATABASES['default']['USER']
DB_HOST = settings.DATABASES['default']['HOST']
DB_PORT = settings.DATABASES['default']['PORT']
DB_PASSWORD = settings.DATABASES['default']['PASSWORD']

class CTAHeatmap(object):
    """
    from mobiletrans.mtdistmap.cta_heatmap import CTAHeatmap
    import mapnik
    m = mapnik.Map(600,600)
    cta_map = CTAHeatmap(m)
    cta_map.render_image()
    """
    
    def __init__(self, empty_map, *args, **kwargs):
        self.define_map(empty_map)
    
    def get_subqueries(self):
        subquery={}
        subquery[1] = """(SELECT * FROM   public.mtlocation_region,  public.mtlocation_neighborhood,  public.django_content_type WHERE 
          mtlocation_region.id = mtlocation_neighborhood.region_ptr_id AND
          mtlocation_region.content_type_id = django_content_type.id) as foo"""
        
        subquery[2] = """(SELECT * FROM 
          mtlocation_location as loc
          inner join django_content_type as ct on (loc.content_type_id = ct.id)
          left outer join public.mtlocation_gplace as place on  ( loc.id = place.location_ptr_id )
        where ct.model not in ('transitstop')) as foo"""
        
        subquery[4] = """(SELECT 
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
        return subquery
    
    def get_stylesheet(self):
        cta_heatmap_xml = os.path.join(settings.PROJECT_ROOT, 'mtdistmap', 'cta_heatmap.xml')
        f = open(cta_heatmap_xml)
        schema = f.read()
        f.close()
        return schema
    
    def define_map(self, map):
        
        subquery = self.get_subqueries()
        schema = self.get_stylesheet()
        
        mapnik.load_map_from_string(map, schema)
        ds = mapnik.PostGIS(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, table='mtlocation_cityborder')
        map.layers[0].datasource = ds
        ds = mapnik.PostGIS(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, table=subquery[1], geometry_table="mtlocation_region", geometry_field='area')
        map.layers[1].datasource = ds
        ds = mapnik.PostGIS(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, table=subquery[2],  geometry_table="mtlocation_location", geometry_field='point')
        map.layers[2].datasource = ds
        ds = mapnik.PostGIS(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, table='mtlocation_ctaraillines', )
        map.layers[3].datasource = ds
        ds = mapnik.PostGIS(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, table=subquery[4], geometry_table="mtlocation_location", geometry_field='point' )
        map.layers[4].datasource = ds        
        self.map = map

    def render_image(self):
        map = self.map
        map.zoom_all()
        mapnik.render_to_file(map, 'chicago.png', 'png')



