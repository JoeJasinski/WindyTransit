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
        if distance_unit:
            pass
    
        distance =  request.GET.get('d')
        if distance:
            pass
        
        ref_pnt = models.Location.objects.all()[0].point
        placemarks = models.Location.objects.filter(point__distance_lte=(ref_pnt, D(m=100) )).distance(ref_pnt).order_by('distance')
        return { 'locations': placemarks, }