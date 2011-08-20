from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from mtcore import utils

def index(request, template_name=""):
    
    params = utils.PrepParams(request)
    
    url_parts = {}
    if params.limit:
        url_parts.update({'limit':params.limit})
    if params.distance_unit:
        url_parts.update({'du':params.distance_unit})
    if params.distance:
        url_parts.update({'d':params.distance})
    if params.point_types:
        url_parts = [ ('type','%s' % i) for i in params.point_types ] + url_parts.items()
    encoded_args = utils.encode_args(url_parts)
    
    built_url = utils.build_url(host=Site.objects.get_current(), 
                                path=reverse('mtlocation_renderkml_latlong', 
                                            kwargs={'lat':params.lat, 'long':params.long,}),
                                args=encoded_args)
    
    context = {'url':built_url, 'lat':params.lat, 'long':long, }
    
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def download(request, template_name=""):
    context = { }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def about(request, template_name=""):
    context = { }
    return render_to_response(template_name, context, context_instance=RequestContext(request))