from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.measure import D 

from mtcore import utils
from . import models

def renderkml(request, lat=None, long=None):
    
    params = utils.PrepParams(request, overrides={'lat':lat, 'long':long})

    template = loader.get_template('mtlocation/locale.kml')
    
    placemarks = models.Location.objects.filter(point__distance_lte=(params.ref_pnt, D(**params.d) )).distance(params.ref_pnt).order_by('distance') 
    c = Context({ 'placemarks': placemarks[:params.limit] })
    
    response = HttpResponse(template.render(c), content_type="application/vnd.google-earth.kml+xml")
    response['Content-Disposition'] = 'attachment; filename=locale.kml'
    return response 


