# import re, decimal, datetime
# from django.contrib.gis.measure import D 
# from piston.handler import BaseHandler
# from piston.utils import rc, throttle
# from django.contrib.gis.geos import fromstr
# 
# from mobiletrans.mtcore import utils
# from mobiletrans.mtcore.external.piston_ext.piston_views import Field, PistonView
# from mobiletrans.mtlocation import models
# 
# 
# #################################################################################
# 
# 
# class TransitRouteHandler(BaseHandler):
#     methods_allowed = ('GET',)
# 
# 
#     def read(self, request, emitter_format="json", uuid=None, route_id=None):
#         transit_route_dict = {}    
#         
#         if uuid:
#             kwargs = {'uuid':uuid}
#         elif route_id:
#             kwargs = {'route_id':route_id}
#         else:
#             kwargs = {}
#            
#         try:
#             transit_route = models.TransitRoute.objects.get(**kwargs)
#         except:
#             transit_route = []
#         else:
#             transit_route_dict = transit_route.serialize()
#             stops = map(lambda x: x.serialize(),  transit_route.transitstop_set.all() )
#             transit_route_dict.update({'stops':stops,})
# 
#         return {'transit_route':transit_route_dict}
# 
# #################################################################################
# 
# class TransitRoutesHandler(BaseHandler):
#     methods_allowed = ('GET',)
# 
#     def read(self, request, emitter_format="json"):
#         
#         kwargs = {}
#         type = request.GET.get('type','').lower()
#         if type in ['1','3','bus','train']:
#             if type == "bus":
#                 type = 3
#             if type == "train":
#                 type = 1
#             kwargs.update({'type':type})
#         
#         routes = models.TransitRoute.objects.filter(**kwargs)
#          
#         transit_routes = []
#         for route in routes:
#             transit_route = route.serialize()
#             
#             #transit_route = {'transit_route':transit_route}
#             transit_routes.append(transit_route)
# 
#         return {'transit_routes':transit_routes}
# 
# 
# #################################################################################
# 
# class LocationView(PistonView):
# 
#     def __init__(self, *args, **kwargs):
#         super(LocationView, self).__init__(*args, **kwargs)
#         location = self.data 
#         self.fields = self.fields + [
#             Field('', lambda x: location, destination='location', ),
#         ]
# 
# class LocationsRootView(PistonView):
# 
#     def __init__(self, *args, **kwargs):
#         super(LocationsRootView, self).__init__(*args, **kwargs)
#         locations = self.data['locations']
#         neighborhood = self.data['neighborhood']
#         zipcode = self.data['zipcode']
#         self.fields = self.fields + [
#             Field('', lambda x: zipcode, destination='zipcode', ),
#             Field('', lambda x: neighborhood, destination='neighborhood', ),
#             Field('', lambda x:  [l for l in locations], destination='locations', ),
#         ]
# 
# 
# class LocationDataHandler(BaseHandler):
#     methods_allowed = ('GET',)
# 
#     def read(self, request, emitter_format="json"):
#         
#         context = {}
#         
#         params = utils.PrepParams(request)
# 
#         location_objs = models.Location.objects.filter(
#             point__distance_lte=(params.ref_pnt, D(**params.d) )).distance(params.ref_pnt).order_by('distance')
# 
#         if params.point_types_input:
#             location_objs = location_objs.filter(content_type__model__in=params.point_types)
# 
#         if params.neighborhood:
#             neighborhood = map(lambda x: x.serialize(), models.Neighborhood.objects.filter(area__contains=params.ref_pnt))
#             context.update({'neighborhood':neighborhood})
# 
#         if params.zipcode:
#             zipcode = map(lambda x: x.serialize(), models.Zipcode.objects.filter(area__contains=params.ref_pnt))
#             context.update({'zipcode':zipcode})
# 
#         locations = []
#         for location, distance in [ (l, l.distance) for l in location_objs.distance(params.ref_pnt) ]:
#             distance = location.distance 
#             location = location.as_leaf_class().serialize()
#             location.update({'distance':distance})
#             locations.append(location,)
# 
#         context.update({ 'locations': locations[:params.limit], })
#         return LocationsRootView(context)
#         #return context
# 
# #################################################################################
#     
# class TransitStopDataHandler(BaseHandler):
#     methods_allowed = ('GET',)
# 
#     def read(self, request, emitter_format="json"):
# 
#         params = utils.PrepParams(request)
#         
#         location_objs = models.TransitStop.orig_objects.filter(location_type=models.TRANSIT_STOP_TYPE_STATION,
#             point__distance_lte=(params.ref_pnt, D(**params.d) )).distance(params.ref_pnt).order_by('distance')
# 
#         if params.point_types_input:
#             location_objs = location_objs.filter(content_type__model__in=params.point_types)
# 
#         locations = []
#         for location, distance in [ (l, l.distance) for l in location_objs.distance(params.ref_pnt) ]:
#             distance = location.distance 
#             location = location.as_leaf_class().serialize()
#             location.update({'distance':distance})
#             locations.append(location,)
# 
# 
#         return { 'locations': locations[:params.limit], }
