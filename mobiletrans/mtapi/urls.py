from django.conf.urls.defaults import *
from piston.resource import Resource

from mtapi.handlers import TransitRouteHandler, LocationDataHandler, TransitRoutesHandler

ad = {  }

transitroutes_resource = Resource(handler=TransitRoutesHandler, **ad)
transitroute_resource = Resource(handler=TransitRouteHandler, **ad)
location_resource = Resource(handler=LocationDataHandler, **ad)


urlpatterns = patterns('',
    url(r'^transitroutes.xml$', transitroutes_resource, { 'emitter_format': 'routexml' }), 
    url(r'^transitroutes/$', transitroutes_resource, { 'emitter_format': 'routexml' }), 
    url(r'^transitroutes.json$', transitroutes_resource, { 'emitter_format': 'json' }), 

    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute.xml$', transitroute_resource, { 'emitter_format': 'routexml' }), 
    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute/$', transitroute_resource, { 'emitter_format': 'routexml' }), 
    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute.json$', transitroute_resource, { 'emitter_format': 'json' }), 

    url(r'^locations/$', location_resource, { 'emitter_format': 'locxml' }),     
    url(r'^locations.xml$', location_resource, { 'emitter_format': 'locxml' }), 
    url(r'^locations.json$', location_resource, { 'emitter_format': 'json' }), 
)
