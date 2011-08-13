import re
from django.contrib.gis.measure import D 
from piston.handler import BaseHandler
from piston.utils import rc, throttle
from django.contrib.gis.geos import fromstr

from mtlocation import models

class TransitRouteHandler(BaseHandler):
    methods_allowed = ('GET',)


    def read(self, request, uuid):
        transit_route_dict = {}       
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
        
        kwargs = {}
        type = request.GET.get('type','').lower()
        if type in ['1','3','bus','train']:
            if type == "bus":
                type = 3
            if type == "train":
                type = 1
            kwargs.update({'type':type})
        
        routes = models.TransitRoute.objects.filter(**kwargs)
         
        transit_routes = []
        for route in routes:
            transit_route = route.serialize()
            
            transit_route = {'transit_route':transit_route}
            transit_routes.append(transit_route)

        return {'transit_routes':transit_routes}
    

class LocationDataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        
        ref_pnt =  fromstr('POINT(-87.627778 41.881944)')
        query = request.GET.get('q')
        if query:
            try:
                x, y, = query.split(',')
            except:
                pass
            else:
                ref_pnt = fromstr('POINT(%s %s)' % (y, x))
        
        distance_unit = request.GET.get('du')
        if not distance_unit in ['km','mi','m','yd','ft',]:
            distance_unit = 'm'
    
        distance =  request.GET.get('d')
        if distance:
            try:
                distance = int(distance)
            except:
                pass
        
        if not distance:
            distance = 1000                    
        d = {distance_unit:distance}

        #ref_pnt = models.Location.objects.get(uuid="e07f055c-5bd5-442f-b340-077bf7e06ee4").point
        
        location_objs = models.Location.objects.filter(
            point__distance_lte=(ref_pnt, D(**d) )).distance(ref_pnt).order_by('distance')

        neighborhood = map(lambda x: x.serialize(), models.Neighborhood.objects.filter(area__contains=ref_pnt))

        locations = []
        for location, distance in [ (l, l.distance) for l in location_objs.distance(ref_pnt) ][:25]:
            distance = location.distance 
            location = location.as_leaf_class().serialize()
            location.update({'distance':distance})
            locations.append({'location':location,'neighborhood':neighborhood})

        return { 'locations': locations, }