from django.conf.urls.defaults import patterns, include, url
import jeditable

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cppdoc.views.listClasses', name='index'),
    url(r'^class/(?P<classname>[\w\-]+)/$', 'cppdoc.views.classDetails'),
    url(r'^class/(?P<classname>[\w\-]+)/f/(?P<functionname>[\w\-]+)/$', 'cppdoc.views.classFunctionDetail'),
    url(r'^class/(?P<classname>[\w\-]+)/v/(?P<variablename>[\w\-]+)/$', 'cppdoc.views.classVariableDetail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^grappelli/', include('grappelli.urls')),
    
    (r'^jeditable/', include('jeditable.urls')),
)