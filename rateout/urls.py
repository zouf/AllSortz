from django.conf.urls import url, patterns, include
from django.contrib import admin
from rateout import settings
from ratings.views import logout_page


admin.autodiscover()

urlpatterns = patterns('',

    #api for comments
    url(r'^api/add_comment/$', 'comments.views.add_comment'),
    url(r'^api/comment_vote/$', 'comments.vote.comment_vote'),
    url(r'^api/remove_comment_vote*', 'comments.vote.remove_comment_vote'),
    
    #api for tags
    url(r'^api/add_tag/$', 'tags.views.add_tag'),
    url(r'^api/get_tags/', 'tags.views.get_all_tags', name='get_all_tags'),
    url(r'^api/tag_vote*', 'tags.vote.tag_vote'),
    url(r'^api/remove_tag_vote*', 'tags.vote.remove_tag_vote'),

    #api for voting on businesses
    url(r'^api/vote*', 'ratings.vote.vote'),
    url(r'^api/rm_vote*', 'ratings.vote.remove_vote'),

    #api for voting on activities
    url(r'^api/act_vote/*', 'activities.vote.vote'),
    url(r'^api/rm_act_vote/*', 'activities.vote.remove_vote'),

    #favicon
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/css/images/favicon.ico'}),
    
    url(r'acts/$', 'activities.views.activities'),    
    url(r'acts/add_activity/', 'activities.views.add_activity'),    
    url(r'^acts/(?P<act_id>\d+)/$', 'activities.views.detail_activity'),
    
    
    url(r'^$','ratings.views.coming_soon'),
    url(r'^$', 'ratings.views.index'),
    url(r'^index*$', 'ratings.views.index'),
    url(r'^index/$', 'ratings.views.index'),
    url(r'^ratings/(?P<bus_id>\d+)/$', 'ratings.views.detail_keywords'),
    url(r'^ratings/search_tags/$', 'ratings.views.search'),
	(r'^search/', include('haystack.urls')),
	url(r'^ratings/add_business/$', 'ratings.views.add_business'),
    url(r'^admin/', include(admin.site.urls)),
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
	url(r'^accounts/', include('registration.urls')),

    (r'^mywiki/', include('wiki.urls')),
 


)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
		(r'^(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
    )


