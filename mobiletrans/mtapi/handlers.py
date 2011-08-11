import re
from django.contrib.gis.measure import D 
from piston.handler import BaseHandler
from piston.utils import rc, throttle

from mtlocation import models

class TransitRouteHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, uuid):
        
        try:
            transit_route = models.TransitRoute.objects.get(uuid=uuid)
        except:
            transit_route = []
        else:
            transit_route_dict = transit_route.serialize()
            stops = map(lambda x: x.serialize(),  transit_route.transitstop_set.all() )
            transit_route_dict.update({'stops':stops,})

        return {'transit_route':transit_route_dict}
    

class TransitRoutesHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        routes = models.TransitRoute.objects.all()
         
        transit_routes = []
        for route in routes:
            transit_route = route.serialize()
            
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

        neighborhood = map(lambda x: x.serialize(), models.Neighborhood.objects.filter(area__contains=ref_pnt))

        locations = []
        for location in location_objs:
            {'location':location.serialize()}
            locations.append({'location':location.serialize(),'neighborhood':neighborhood})

        return { 'locations': locations, }