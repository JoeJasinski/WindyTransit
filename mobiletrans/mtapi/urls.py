from django.conf.urls.defaults import *
from piston.resource import Resource

from mtapi.handlers import TransitRouteHandler, LocationDataHandler

ad = {  }

transitroute_resource = Resource(handler=TransitRouteHandler, **ad)
location_resource = Resource(handler=LocationDataHandler, **ad)


urlpatterns = patterns('',
    url(r'^transitroutes.xml$', transitroute_resource, { 'emitter_format': 'routexml' }), 
    url(r'^transitroutes/$', transitroute_resource, { 'emitter_format': 'routexml' }), 
    url(r'^transitroutes.json$', transitroute_resource, { 'emitter_format': 'json' }), 

    url(r'^locations/$', location_resource, { 'emitter_format': 'xml' }),     
    url(r'^locations.xml$', location_resource, { 'emitter_format': 'xml' }), 
    url(r'^locations.json$', location_resource, { 'emitter_format': 'json' }), 
)
