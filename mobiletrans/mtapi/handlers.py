import re, decimal 
from django.contrib.gis.measure import D 
from piston.handler import BaseHandler
from piston.utils import rc, throttle
from django.contrib.gis.geos import fromstr

from mtcore import utils
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
            
            #transit_route = {'transit_route':transit_route}
            transit_routes.append(transit_route)

        return {'transit_routes':transit_routes}
    

class LocationDataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        
        lat = request.GET.get('lat')
        long = request.GET.get('long')
        ref_pnt, y, x = utils.get_pt_from_coord(lat, long)
        
        distance_unit = request.GET.get('du')
        distance =  request.GET.get('d')
        d = utils.get_distance(distance, distance_unit)

    
        limit = request.GET.get('limit')
        limit = utils.get_limit(limit)


        point_types_input = request.GET.getlist('type')
        #ref_pnt = models.Location.objects.get(uuid="e07f055c-5bd5-442f-b340-077bf7e06ee4").point
        
        point_types = utils.get_point_types(point_types_input)
        
        location_objs = models.Location.objects.filter(
            point__distance_lte=(ref_pnt, D(**d) )).distance(ref_pnt).order_by('distance')

        if point_types_input:
            location_objs = location_objs.filter(content_type__model__in=point_types)

        neighborhood = map(lambda x: x.serialize(), models.Neighborhood.objects.filter(area__contains=ref_pnt))

        locations = []
        for location, distance in [ (l, l.distance) for l in location_objs.distance(ref_pnt) ]:
            distance = location.distance 
            location = location.as_leaf_class().serialize()
            location.update({'distance':distance})
            locations.append(location,)

        return { 'locations': locations[:limit], 'neighborhood':neighborhood }
    
    
class TransitStopDataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        
        lat = request.GET.get('lat')
        long = request.GET.get('long')
        ref_pnt, y, x = utils.get_pt_from_coord(lat, long)
        
        distance_unit = request.GET.get('du')
        distance =  request.GET.get('d')
        d = utils.get_distance(distance, distance_unit)

    
        limit = request.GET.get('limit')
        limit = utils.get_limit(limit)


        point_types_input = request.GET.getlist('type')
        #ref_pnt = models.Location.objects.get(uuid="e07f055c-5bd5-442f-b340-077bf7e06ee4").point
        
        point_types = utils.get_point_types(point_types_input)
        
        location_objs = models.TransitStop.orig_objects.filter(location_type=models.TRANSIT_STOP_TYPE_STATION,
            point__distance_lte=(ref_pnt, D(**d) )).distance(ref_pnt).order_by('distance')

        if point_types_input:
            location_objs = location_objs.filter(content_type__model__in=point_types)

        locations = []
        for location, distance in [ (l, l.distance) for l in location_objs.distance(ref_pnt) ]:
            distance = location.distance 
            location = location.as_leaf_class().serialize()
            location.update({'distance':distance})
            locations.append(location,)

        return { 'locations': locations[:limit], }