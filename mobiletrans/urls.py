from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^$', 'mobiletrans.views.index', { 'template_name':'index.html'}, name="index"),
    url('^download/$', 'mobiletrans.views.download', { 'template_name':'download.html'}, name="download"),
    url('^about/$', 'mobiletrans.views.about', { 'template_name':'about.html'}, name="about"),
    url('^kml/$', 'mobiletrans.mtlocation.views.renderkml', { }, name="mtlocation_renderkml"),
    url('^kml/longlat/(?P<long>[-\d.]+),(?P<lat>[-\d.]+)/$', 'mobiletrans.mtlocation.views.renderkml', { }, name="mtlocation_renderkml_longlat"),
    url('^kml/latlong/(?P<lat>[-\d.]+),(?P<long>[-\d.]+)/$', 'mobiletrans.mtlocation.views.renderkml', { }, name="mtlocation_renderkml_latlong"),
    url('^api/1/', include('mobiletrans.mtapi.urls')),    
)
