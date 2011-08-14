from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^$', 'views.index', { 'template_name':'index.html'}, name="index"),
    url('^kml/$', 'mtlocation.views.renderkml', { }, name="mtlocation_renderkml"),
    url('^kml/longlat/(?P<long>[-\d.]+),(?P<lat>[-\d.]+)/$', 'mtlocation.views.renderkml', { }, name="mtlocation_renderkml_longlat"),
    url('^kml/latlong/(?P<lat>[-\d.]+),(?P<long>[-\d.]+)/$', 'mtlocation.views.renderkml', { }, name="mtlocation_renderkml_latlong"),
    url('^api/1/', include('mtapi.urls')),    
)
