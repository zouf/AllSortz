from django.conf.urls import url, patterns, include
from django.contrib import admin
from rateout import settings
from ratings.views import logout_page


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/add_tag/$', 'ratings.tags.add_tag'),
    url(r'^api/add_tip/$', 'ratings.tips.add_tip'),
    url(r'^$','ratings.views.coming_soon'),
    url(r'^$', 'ratings.views.index'),
    url(r'^index*$', 'ratings.views.index'),
    url(r'^index/$', 'ratings.views.index'),
    url(r'^ratings/(?P<bus_id>\d+)/$', 'ratings.views.detail_keywords'),
    url(r'^ratings/search_tags/$', 'ratings.views.search_test'),
	(r'^search/', include('haystack.urls')),
	url(r'^ratings/add_business/$', 'ratings.views.add_business'),
    url(r'^admin/', include(admin.site.urls)),
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
	url(r'^accounts/', include('registration.urls')),
    url(r'^vote*', 'ratings.vote.vote'),
    url(r'^remove_vote*', 'ratings.vote.remove_vote'),
    url(r'^tip_vote*', 'ratings.vote.tip_vote'),
    url(r'^remove_tip_vote*', 'ratings.vote.remove_tip_vote'),
    url(r'^tag_vote*', 'ratings.vote.tag_vote'),
    url(r'^remove_tag_vote*', 'ratings.vote.remove_tag_vote'),
    url(r'^api/get_all_tags/', 'ratings.views.get_tags', name='get_all_tags')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
		(r'^(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
    )


