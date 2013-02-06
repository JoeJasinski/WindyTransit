from django.conf.urls.defaults import *
from piston.resource import Resource

from mobiletrans.mtapi.handlers import TransitRouteHandler, LocationDataHandler, TransitRoutesHandler, TransitStopDataHandler

ad = {  }

transitroutes_resource = Resource(handler=TransitRoutesHandler, **ad)
transitroute_resource = Resource(handler=TransitRouteHandler, **ad)
location_resource = Resource(handler=LocationDataHandler, **ad)
transitstop_resource = Resource(handler=TransitStopDataHandler, **ad)

urlpatterns_1 = patterns('',
    url(r'^transitroutes(\.(?P<emitter_format>.+))?$', 
        transitroutes_resource, { }, name="api_transitroutes"), 
    url(r'^transitroutes/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/transitroute(\.(?P<emitter_format>.+))?$', 
        transitroute_resource, { }, name="api_transitroute"), 
    url(r'^transitroutes/(?P<route_id>\w+)/transitroute(\.(?P<emitter_format>.+))?$', 
        transitroute_resource, { }, name="api_transitroute"), 
    url(r'^locations(\.(?P<emitter_format>.+))?$', 
        location_resource, { }, name="api_locations"),  
    url(r'^transitstops(\.(?P<emitter_format>.+))?$', 
        transitstop_resource, { }, name="api_transitstops"), 
)

urlpatterns = patterns('',
  url(r'^1/', include(urlpatterns_1)),
)