from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ratings.views.index'),
    url(r'^ratings/(?P<bus_id>\d+)/$', 'ratings.views.detail'),
    url(r'^ratings/(?P<bus_id>\d+)/rate/$', 'ratings.views.rate'),
    url(r'^admin/', include(admin.site.urls)),
)