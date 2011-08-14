from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from mtcore import utils

def index(request, template_name=""):
    
    lat = request.GET.get('lat')
    long = request.GET.get('long')
    ref_pnt, lat, long = utils.get_pt_from_coord(lat, long)
    
    distance_unit = request.GET.get('du')
    distance =  request.GET.get('d')
    d = utils.get_distance(distance, distance_unit)    

    point_types = request.GET.getlist('type')

    url_parts = {}
    if distance_unit:
        url_parts.update({'du':distance_unit})
    if distance:
        url_parts.update({'d':distance})
    if point_types:
        url_parts = [ ('type','%s' % i) for i in point_types ] + url_parts.items()
    encoded_args = utils.encode_args(url_parts)
    
    built_url = utils.build_url(host=Site.objects.get_current(), 
                                path=reverse('mtlocation_renderkml_latlong', 
                                            kwargs={'lat':lat, 'long':long,}),
                                args=encoded_args)
    
    context = {'url':built_url, 'lat':lat, 'long':long, }
    
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def download(request, template_name=""):
    context = { }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def about(request, template_name=""):
    context = { }
    return render_to_response(template_name, context, context_instance=RequestContext(request))