from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.measure import D 

from mtcore import utils
from . import models

def renderkml(request, lat=None, long=None):
    
    if not lat:
        lat = request.GET.get('lat', None)
    if not long:
        long = request.GET.get('long', None)
    ref_pnt, y, x = utils.get_pt_from_coord(lat, long)
    
    distance_unit = request.GET.get('du')
    distance =  request.GET.get('d')
    d = utils.get_distance(distance, distance_unit)

    point_types = request.GET.getlist('type')
    utils.get_point_types(point_types)
    #raise AssertionError(d, lat, long)
    
    limit = request.GET.get('limit')
    limit = utils.get_limit(limit)
    
    template = loader.get_template('mtlocation/locale.kml')
    
    placemarks = models.Location.objects.filter(point__distance_lte=(ref_pnt, D(**d) )).distance(ref_pnt).order_by('distance') 
    c = Context({ 'placemarks': placemarks[:limit] })
    
    response = HttpResponse(template.render(c), content_type="application/vnd.google-earth.kml+xml")
    response['Content-Disposition'] = 'attachment; filename=locale.kml'
    return response 


