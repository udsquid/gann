###
### django libraries
###
from django.conf.urls import patterns, include, url


###
### URLs
###
urlpatterns = patterns('high_low.views',
    url(r'^point/list/$', 'list_points'),
    url(r'^point/len/$', 'get_length'),
    url(r'^point/add/$', 'add_point'),
    url(r'^point/filter/$', 'filter_points'),
)
