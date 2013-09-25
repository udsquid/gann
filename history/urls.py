###
### django libraries
###
from django.conf.urls import patterns, include, url


###
### URLs
###
urlpatterns = patterns('history.views',
    url(r'^(?P<category>.*)/(?P<action>.*)/$', 'history_do'),
)
