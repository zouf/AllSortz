from allsortz.views import logout_page
from django.conf.urls import url, patterns, include
from django.contrib import admin
from rateout import settings
from rateout.settings import STATIC_URL


admin.autodiscover()

urlpatterns = patterns('',

    #api for comments
    url(r'^api/comment_vote/$', 'ratings.vote.comment_vote'),
    url(r'^api/remove_comment_vote*', 'ratings.vote.remove_comment_vote'),
    
    #api for tags
    url(r'^api/add_a_sort/$', 'tags.views.add_a_sort'),
    url(r'^api/add_tag/$', 'tags.views.add_tag_business'),
    url(r'^api/add_user_tag/$', 'tags.views.add_user_tag'),
    url(r'^api/remove_user_tag/$', 'tags.views.remove_user_tag'),

    url(r'^api/get_tags/', 'tags.views.get_all_tags', name='get_all_tags'),
    url(r'^api/tag_vote*', 'tags.vote.tag_vote'),
    url(r'^api/remove_tag_vote*', 'tags.vote.remove_tag_vote'),
    

    #api for voting on businesses
    url(r'^api/vote*', 'ratings.vote.vote'),
    url(r'^api/rm_vote*', 'ratings.vote.remove_vote'),
    url(r'^api/add_bus_rating/', 'ratings.vote.add_bus_rating'),

    #api for voting on activities
#    url(r'^api/act_vote/*', 'activities.vote.vote'),
#    url(r'^api/rm_act_vote/*', 'activities.vote.remove_vote'),


    #comments on discussion page
    url(r'^api/add_tag_comment/$','comments.views.add_tag_comment'),
    url(r'^api/add_photo_comment/$','comments.views.add_photo_comment'),



    #favicon
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': STATIC_URL+'css/images/favicon.ico'}),
    
    #URLS for editing wiki pages
    url(r'^ratings/(?P<bus_id>\d+)/edit/(?P<page_id>\d+)/$','allsortz.views.edit_tag_discussion'),
    url(r'^ratings/(?P<bus_id>\d+)/edit_master/(?P<page_id>\d+)/$','allsortz.views.edit_master_tag_discussion'),

    
    #activity URLs
#    url(r'acts/$', 'activities.views.activities'),    
#    url(r'acts/add_activity/', 'activities.views.add_activity'),    
#    url(r'^acts/(?P<act_id>\d+)/$', 'activities.views.detail_activity'),
    
    #URL for user details
    url(r'^user_details/(?P<uid>\d+)/$','allsortz.views.user_details'),
    
    #display businesses assoc with a tag
    url(r'^ratings/disp/(?P<tag_id>\d+)/$','allsortz.views.display_tag'),

    #answer questions on businesses
    url(r'^ratings/answer_questions/(?P<bus_id>\d+)$','allsortz.contribute.ans_business_questions'),

    #relate traits to yourself 
    url(r'^ratings/user_traits/$','usertraits.views.add_trait_relationships'),

    
    #url(r'^$','ratings.views.coming_soon'),
    url(r'^$', 'allsortz.views.index'),
    url(r'^index*$', 'allsortz.views.index'),
    url(r'^index/$', 'allsortz.views.index'),
    url(r'^ratings/(?P<bus_id>\d+)/$', 'allsortz.views.bus_details'),
    url(r'^ratings/search_tags/$', 'allsortz.views.search'),
	(r'^search/', include('haystack.urls')),
    
    #for adding content to the site
	url(r'^ratings/add_business/$', 'allsortz.contribute.add_business'),
    url(r'^ratings/add_question/$', 'allsortz.contribute.add_question'),
    url(r'^ratings/add_trait/$','allsortz.views.add_trait'),
    url(r'^ratings/add_new_tag/$', 'allsortz.contribute.add_new_tag'),
    url(r'^ratings/add_community/$', 'allsortz.contribute.add_community'),


    #misc. admin stuff
    url(r'^feedback/$','allsortz.webadmin.feedback'),
    url(r'^contact/$','allsortz.webadmin.feedback'),
    url(r'^about/$', 'allsortz.webadmin.allsortz_about'),
    url(r'^help/$','allsortz.webadmin.allsortz_help'),

    
    url(r'^admin/', include(admin.site.urls)),
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'allsortz.views.logout_page'),
	url(r'^accounts/', include('registration.urls')),
#    url(r'^comments/add_comment/(?P<bus_id>\d+)/$','ratings.views.add_comment_form'),

    
    
    url(r'^ratings/reset_db/$','allsortz.populate.prepopulate_database'),
    
    #facebook stuff
    
    url(r'^handle_fb_login/$','ratings.facebook.handle_fb_login'),
    url(r'^fbauth/$','ratings.facebook.handle_fb_request'),
    (r'^invites/', include('privatebeta.urls')),
    (r'^mywiki/', include('wiki.urls')),
    (r'^pics/', include('photos.urls')),
    (r'^ios/', include('ios_interface.urls'))

        
    


)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
		(r'^(?P<path>.*)$', 'django.views.static.serve',  {'document_root':     settings.MEDIA_ROOT}),
    )


