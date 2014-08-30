from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.models import Site
from django.conf import settings

from mobiletrans.mtcore import utils
from mobiletrans.mtlocation import models

def renderkml(request, lat=None, long=None):

    overrides = {}
    if lat:
        overrides.update({'lat':lat})
    if long:
        overrides.update({'long':long}) 
 
    params = utils.PrepParams(request, overrides)
    
    context = {}
    
    template = loader.get_template('mtlocation/locale.kml')
    
    if params.neighborhood:
        try:
            neighborhood = models.Neighborhood.sub_objects.filter(area__contains=params.ref_pnt)[0]
        except IndexError:
            neighborhood = ""
        context.update({ 'neighborhood':neighborhood,})
   
    if params.zipcode:
        try:
            zipcode = models.Zipcode.sub_objects.filter(area__contains=params.ref_pnt)[0]
        except IndexError:
            zipcode = ""
        context.update({ 'zipcode':zipcode,})        

    placemarks = models.Location.objects.displayable().get_closest(from_point=params.ref_pnt, distance_dict=params.d )  
    
    context.update({ 'placemarks': placemarks[:params.limit], 'site': Site.objects.get_current(), 'STATIC_URL':settings.STATIC_URL, })

    c = Context(context)

    response = HttpResponse(template.render(c), content_type="application/vnd.google-earth.kml+xml")
    response['Content-Disposition'] = 'attachment; filename=locale.kml'
    return response 
