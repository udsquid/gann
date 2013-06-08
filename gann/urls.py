from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gann.views.home', name='home'),
    # url(r'^gann/', include('gann.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('high_low.views',
    url(r'^high_low/point/list/$', 'list_points'),
    url(r'^high_low/point/len/$', 'get_length'),
    url(r'^high_low/point/add/$', 'add_point'),
    url(r'^high_low/point/filter/$', 'filter_point'),
)
