from django.conf.urls import *
from rest_framework import routers
from rest_framework import generics
from rest_framework.urlpatterns import format_suffix_patterns
from mobiletrans.mtapi import views


urlpatterns_2 = patterns('',
    url(r'^transitroutes(\.(?P<emitter_format>.+))?$', 
        views.ListTransitRoutesView.as_view(), name='api2_transitroutes'),
    url(r'^transitroutes/(?P<route_id>\w+)/transitroute$', 
        views.ListTransitRouteView.as_view(), { }, name="api2_transitroute"),
    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute$', 
        views.ListTransitRouteView.as_view(), { }, name="api2_transitroute"),
    url(r'^locations$', 
        views.LocationDataView.as_view() , { }, name="api_locations"),  
    url(r'^transitstops$', 
        views.TransitStopDataView.as_view(), { }, name="api2_transitstops"), 
    
    url(r'^lines$',
        views.CTARailLinesRoutesView.as_view(), {}, name="api2_lines"),
    url(r'^lines/(?P<route_id>\w+)$',
        views.CTARailLinesRoutesView.as_view(), {}, name="api2_lines"),
)

urlpatterns_2 = format_suffix_patterns(urlpatterns_2, allowed=['json', 'html'])

urlpatterns = patterns('',
  url(r'^2/', include(urlpatterns_2)),
)
