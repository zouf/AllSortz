from django.conf.urls import patterns

urlpatterns = patterns('photos.views',
    (r'^$', 'full_gallery'),
    ('^gallery/(?P<bus_id>\d+)/$', 'bus_gallery'),
    ('^detail/(?P<ph_id>\d+)/$', 'photo_detail'),
    ('add_bus_photo/$','add_photo_to_bus')
)

