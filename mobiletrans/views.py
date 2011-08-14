from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from mtcore import utils

def index(request, template_name=""):
    
    lat = request.GET.get('lat')
    long = request.GET.get('long')
    
    ref_pnt, y, x = utils.get_pt_from_coord(lat, long)
    
    distance_unit = request.GET.get('du')
    distance =  request.GET.get('d')

    d = utils.get_distance(distance, distance_unit)    
    
    context = {'lat':lat, 'long':long, 'distance_unit':distance_unit, 'distance':distance, }
    return render_to_response(template_name, context, context_instance=RequestContext(request))
