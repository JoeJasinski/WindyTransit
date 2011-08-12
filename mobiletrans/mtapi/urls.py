from django.conf.urls.defaults import *
from piston.resource import Resource

from mtapi.handlers import TransitRouteHandler, LocationDataHandler, TransitRoutesHandler

ad = {  }

transitroutes_resource = Resource(handler=TransitRoutesHandler, **ad)
transitroute_resource = Resource(handler=TransitRouteHandler, **ad)
location_resource = Resource(handler=LocationDataHandler, **ad)


urlpatterns = patterns('',
    url(r'^transitroutes.xml$', transitroutes_resource, { 'emitter_format': 'routexml' }, name="api_transitroutes_xml"), 
    url(r'^transitroutes/$', transitroutes_resource, { 'emitter_format': 'routexml' }, name="api_transitroutes"), 
    url(r'^transitroutes.json$', transitroutes_resource, { 'emitter_format': 'json' }, name="api_transitroutes_json"), 

    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute.xml$', 
        transitroute_resource, { 'emitter_format': 'routexml' }, name="api_transitroute_xml"), 
    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute/$', 
        transitroute_resource, { 'emitter_format': 'routexml' }, name="api_transitroute"), 
    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute.json$', 
        transitroute_resource, { 'emitter_format': 'json' }, name="api_transitroute_json"), 

    url(r'^locations/$', location_resource, { 'emitter_format': 'locxml' }, name="api_locations"),     
    url(r'^locations.xml$', location_resource, { 'emitter_format': 'locxml' }, name="api_locations_xml"), 
    url(r'^locations.json$', location_resource, { 'emitter_format': 'json' }, name="api_locations_json"), 
)
