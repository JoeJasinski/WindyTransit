from django.conf.urls import patterns, include, url
from .views import MapView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^$', 'mobiletrans.views.index', { 'template_name':'index.html'}, 
        name="index"),
    url('^about/$', 'mobiletrans.views.about', { 'template_name':'about.html'}, 
        name="about"),
    url('^routemap/$', MapView.as_view( template_name='routemap.html'), 
        name="routemap"),
    
    url('^kml/$', 'mobiletrans.mtlocation.views.renderkml', { }, 
        name="mtlocation_renderkml"),
    url('^kml/longlat/(?P<long>[-\d.]+),(?P<lat>[-\d.]+)/$', 
        'mobiletrans.mtlocation.views.renderkml', { }, 
        name="mtlocation_renderkml_longlat"),
    url('^kml/latlong/(?P<lat>[-\d.]+),(?P<long>[-\d.]+)/$', 
        'mobiletrans.mtlocation.views.renderkml', { }, 
        name="mtlocation_renderkml_latlong"),
                       
    url('^api/', include('mobiletrans.mtapi.urls')),

)
