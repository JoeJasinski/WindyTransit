from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from django.views.generic import TemplateView

from mobiletrans.mtlocation.models import CityBorder
from mobiletrans.mtcore import utils


def index(request, template_name=""):
    params = utils.PrepParams(request)
    url_parts = {}
    if params.limit:
        url_parts.update({'limit': params.limit})
    if params.distance_unit:
        url_parts.update({'du': params.distance_unit})
    if params.distance:
        url_parts.update({'d': params.distance})
    if params.point_types:
        url_parts = [('type', '%s' % i) for i in params.point_types] + url_parts.items()
    encoded_args = utils.encode_args(url_parts)
    built_url = utils.build_url(host=Site.objects.get_current().domain,
                                path=reverse('mtlocation_renderkml'),
                                args=encoded_args, encode=False)
    context = {'url': built_url, 'lat': params.lat, 'long': long, }
    return render(request, template_name, context)


def download(request, template_name=""):
    context = {}
    return render(request, template_name, context)


def about(request, template_name=""):
    context = {}
    return render(request, template_name, context)


class MapView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        region = get_object_or_404(CityBorder, name='chicago')
        center = region.area.centroid
        context.update({"center": center})
        return context
