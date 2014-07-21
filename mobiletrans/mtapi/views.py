from django.contrib.gis.measure import D 
from mobiletrans.mtlocation.models import ( 
    TransitRoute, TransitStop, Location, Neighborhood, Zipcode, 
    TRANSIT_STOP_TYPE_STATION, CityBorder, CTARailLines )
from mobiletrans.mtcore import utils
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import (CTARailLinesSerializer, CityBorderSerializer, 
                          NeighborhoodSerializer, LocationSerializer)

class ListTransitRoutesSerializer(serializers.Serializer):
    pass

class ListTransitRoutesView(generics.ListAPIView):

    serializer_class = ListTransitRoutesSerializer
    lookup_url_kwarg = "route_id"

    def get_queryset(self):
        kwargs = {}
        type = self.request.GET.get('type','').lower()
        if type in ['1','3','bus','train']:
            if type == "bus":
                type = 3
            if type == "train":
                type = 1
            kwargs.update({'type':type})        
        return TransitRoute.objects.filter(**kwargs)

    def get(self, request, *args, **kwargs):
        transit_routes = []
        self.object_list = self.filter_queryset(self.get_queryset())
        for route in self.object_list:
            transit_route = route.serialize()
            transit_routes.append(transit_route)
        return Response({'transit_routes':transit_routes})
    
    
class ListTransitRouteView(generics.ListAPIView):
    methods_allowed = ('GET',)

    def get(self, request, *args, **kwargs):
        transit_route_dict = {}    
        
        if kwargs.get('uuid'):
            kwargs = {'uuid':kwargs['uuid']}
        elif kwargs.get('route_id'):
            kwargs = {'route_id':kwargs['route_id']}
        else:
            kwargs = {}
           
        try:
            transit_route = TransitRoute.objects.get(**kwargs)
        except:
            transit_route = []
        else:
            transit_route_dict = transit_route.serialize()
            stops = map(lambda x: x.serialize(),  transit_route.transitstop_set.all() )
            transit_route_dict.update({'stops':stops,})

        return Response({'transit_route':transit_route_dict})


class LocationDataView(generics.ListAPIView):
    methods_allowed = ('GET',)

    def get(self, request, *args, **kwargs):
        
        context = {}
        
        params = utils.PrepParams(request)

        location_objs = Location.objects.filter(
            point__distance_lte=(params.ref_pnt, D(**params.d) )).distance(params.ref_pnt).order_by('distance')

        if params.point_types_input:
            location_objs = location_objs.filter(content_type__model__in=params.point_types)

        if params.neighborhood:
            neighborhood = map(lambda x: x.serialize(), Neighborhood.objects.filter(area__contains=params.ref_pnt))
            context.update({'neighborhood':neighborhood})

        if params.zipcode:
            zipcode = map(lambda x: x.serialize(), Zipcode.objects.filter(area__contains=params.ref_pnt))
            context.update({'zipcode':zipcode})

        locations = []
        for location, distance in [ (l, l.distance) for l in location_objs.distance(params.ref_pnt) ]:
            distance = location.distance 
            location = location.as_leaf_class().serialize()
            location.update({'distance':str(distance)})
            locations.append(location,)

        context.update({ 'locations': locations[:params.limit], })
        return Response(context)


class TransitStopDataView(generics.ListAPIView):
    methods_allowed = ('GET',)
 
    def get(self, request, *args, **kwargs):
        params = utils.PrepParams(request)
        location_objs = TransitStop.orig_objects.filter(location_type=TRANSIT_STOP_TYPE_STATION,
            point__distance_lte=(params.ref_pnt, D(**params.d) )).distance(params.ref_pnt).order_by('distance')
        if params.point_types_input:
            location_objs = location_objs.filter(content_type__model__in=params.point_types)
        locations = []
        for location, distance in [ (l, l.distance) for l in location_objs.distance(params.ref_pnt) ]:
            distance = location.distance 
            location = location.as_leaf_class().serialize()
            location.update({'distance':str(distance)})
            locations.append(location,)
        return Response({ 'locations': locations[:params.limit], })


class CTARailLinesRoutesView(generics.ListAPIView):

    model = CTARailLines
    methods_allowed = ('GET',)
    serializer_class = CTARailLinesSerializer
    lookup_url_kwarg = "objectid"

    def get_queryset(self):

        if self.kwargs.get('objectid'):
            kwargs = {'objectid':self.kwargs['objectid']}
        else:
            kwargs = {}

        return self.model.objects.filter(**kwargs)
    

class CityBorderView(generics.ListAPIView):

    model = CityBorder
    methods_allowed = ('GET',)
    serializer_class = CityBorderSerializer
    lookup_url_kwarg = "name"

    def get_queryset(self):

        if self.kwargs.get('name'):
            kwargs = {'name':self.kwargs['name']}
        else:
            kwargs = {}

        return self.model.objects.filter(**kwargs)


class NeighborhoodFromCoordView(generics.RetrieveAPIView):

    model = Neighborhood
    methods_allowed = ('GET',)
    serializer_class = NeighborhoodSerializer
    lookup_url_kwarg = "name"

    def dispatch(self, request, *args, **kwargs):
        self.params = utils.PrepParams(self.request)
        return super(NeighborhoodFromCoordView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = self.filter_queryset(self.get_queryset())
        if self.params.neighborhood:
            try:
                neighborhood = Neighborhood.sub_objects.filter(area__contains=self.params.ref_pnt)[0]
            except IndexError:
                neighborhood = ""
        #neighborhood = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, neighborhood)
        return neighborhood

    def get(self, request, format=None):
        placemarks = Location.objects.displayable().get_closest(from_point=self.params.ref_pnt, distance_dict=self.params.d ) 
        neighborhood = self.get_object()
        data = {'neighborhood':NeighborhoodSerializer(neighborhood).data,
                'placemarks':LocationSerializer(placemarks).data,}
        return Response(data)


class RailLinesRouteBorderView(APIView):
    
    def get(self, request, *args, **kwargs):
        routes = CTARailLines.objects.all()
        
        name = self.kwargs.get('name')
        border = get_object_or_404(CityBorder, name=name)
        kwargs = {'name':name}
            
        border = CityBorder.objects.filter(**kwargs)

        data = {'border':CityBorderSerializer(border).data,
                'routes':CTARailLinesSerializer(routes).data,}
        return Response(data)
    
