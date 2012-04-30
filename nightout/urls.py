from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from nightout import settings
from ratings.views import *



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ratings.views.index'),
    url(r'^ratings/(?P<bus_id>\d+)/$', 'ratings.views.detail'),
    url(r'^ratings/(?P<bus_id>\d+)/rate/$', 'ratings.views.rate'),
	url(r'^ratings/add_keyword/$', 'ratings.views.add_keyword'),
	url(r'^ajax_query/$','ratings.views.ajax_query'),
	url(r'^ratings/add_business/$', 'ratings.views.add_business'),
    url(r'^ratings/view_ratings/(?P<maxc>\d+)', 'ratings.views.display_table'),
    url(r'^ratings/view_ratings*$', 'ratings.views.display_table_full'),
    url(r'^ratings/pop_test_data/$', 'ratings.views.pop_test_data'),
    url(r'^admin/', include(admin.site.urls)),
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
	(r'^accounts/', include('registration.urls')),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
		(r'^(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
    )

