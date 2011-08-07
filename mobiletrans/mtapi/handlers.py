import re
from django.contrib.gis.measure import D 
from piston.handler import BaseHandler
from piston.utils import rc, throttle

from mtlocation import models

class TransitRouteHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        routes = models.TransitRoute.objects.all()
         
        transit_routes = []
        for route in routes:
            node_names = ('uuid', 'route_id',
            'short_name', 'long_name', 'description', 
            'type', 'color', 'text_color','url')
            transit_route = {}
            for node_name in node_names:
                transit_route.update({node_name:getattr(route, "%s" % node_name)})
            
            transit_route = {'transit_route':transit_route}
            transit_routes.append(transit_route)

        return {'transit_routes':transit_routes}
    
    
class LocationDataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        
        query = request.GET.get('q')
        if query:
            pass
        
        distance_unit = request.GET.get('du')
        if distance_unit in ['km','mi','m','yd','ft',]:
            pass
        else:
            distance_unit = 'm'
    
        distance =  request.GET.get('d')
        if distance:
            try:
                distance = int(distance)
            except IndexError:
                distance = 1000
        
        ref_pnt = models.Location.objects.all()[0].point
        location_objs = models.Location.objects.filter(
            point__distance_lte=(ref_pnt, D(m=100) )).distance(ref_pnt).order_by('distance')

        locations = []
        for location in location_objs:
            {'location':location.serialize()}
            locations.append({'location':location.serialize()})

        return { 'locations': locations, }