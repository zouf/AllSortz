from django.conf.urls import patterns

urlpatterns = patterns('ios_interface.views',
    (r'^get_businesses/$', 'get_businesses')

)

