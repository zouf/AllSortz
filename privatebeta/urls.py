from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'privatebeta.views.invite', name='privatebeta_invite'),
    url(r'^sent/$', 'privatebeta.views.sent', name='privatebeta_sent'),
    url(r'^signuprequired/$','privatebeta.views.signupreq',name='privatebeta_signupreq')
)
