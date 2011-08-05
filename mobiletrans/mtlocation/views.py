from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.measure import D 

from . import models

def renderkml(request):
    
    ref_pnt = models.Location.objects.all()[0].point
    
    template = loader.get_template('mtlocation/locale.kml')
    
    placemarks = models.Location.objects.filter(point__distance_lte=(ref_pnt, D(m=100) )).distance(ref_pnt).order_by('distance') 
    c = Context({ 'placemarks': placemarks })
    
    response = HttpResponse(template.render(c), content_type="application/vnd.google-earth.kml+xml")
    response['Content-Disposition'] = 'attachment; filename=locale.kml'
    return response 