from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^$', 'views.index', { 'template_name':'index.html'}, name="index"),
    url('^kml/$', 'mtlocation.views.renderkml', { }, name="mtlocation_renderkml"),
    url('^routes/$', 'mtlocation.views.transitroutes', { }, name="mtlocation_transitroutes"),
    url('^api/1/', include('mtapi.urls')),    
)
