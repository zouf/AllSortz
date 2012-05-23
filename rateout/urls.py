from django.conf.urls import url, patterns, include
from django.contrib import admin
from rateout import settings
from ratings.views import logout_page



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
    url(r'^ratings/top_ten/$', 'ratings.views.top_ten'),
    url(r'^admin/', include(admin.site.urls)),
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
	url(r'^accounts/', include('registration.urls')),
    url(r'^vote*', 'ratings.views.vote'),
    url(r'^remove_vote*', 'ratings.views.remove_vote')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
		(r'^(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
    )

