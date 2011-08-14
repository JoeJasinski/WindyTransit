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

    #raise AssertionError(lat, long)
    
    template = loader.get_template('mtlocation/locale.kml')
    
    placemarks = models.Location.objects.filter(point__distance_lte=(ref_pnt, D(**d) )).distance(ref_pnt).order_by('distance') 
    c = Context({ 'placemarks': placemarks })
    
    response = HttpResponse(template.render(c), content_type="application/vnd.google-earth.kml+xml")
    response['Content-Disposition'] = 'attachment; filename=locale.kml'
    return response 



"""
from xml.dom.minidom import Document
def transitroutes(request):

    ref_pnt = models.Location.objects.all()[0].point
    placemarks = models.TransitRoute.objects.all()
    
    doc = Document()
    request = doc.createElement("request")
    transit_routes = doc.createElement("transit_routes")
    for placemark in placemarks:
        transit_route = doc.createElement("transit_route")

        for child_node in [
            ('uuid','uuid'), ('route_id','route_id',),
            ('short_name','short_name'), ('long_name', 'long_name'),
            ('description','description'), ('type','type'),
            ('color','color'), ('text_color','text_color'), ('url','url')]:
            child = doc.createElement(child_node[0])
            child_text = doc.createTextNode("%s" % getattr(placemark, "%s" % child_node[1]))
            child.appendChild(child_text)
            transit_route.appendChild(child)
            
        transit_routes.appendChild(transit_route)
        
        
        
    request.appendChild(transit_routes)    
    doc.appendChild(request)
    
    response = HttpResponse(doc.toprettyxml(indent="  "), content_type="application/xml")
    response['Content-Disposition'] = 'attachment; filename=locale.xml'
    return response 
"""