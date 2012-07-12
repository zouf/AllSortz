from django.conf.urls.defaults import *



urlpatterns = patterns('photos.views',
    (r'^$', 'full_gallery'),
    ('(?P<bus_id>\d+)/$', 'bus_gallery'),
)
