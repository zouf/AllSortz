from django.conf.urls import patterns

urlpatterns = patterns('ios_interface.views',
    (r'^businesses/$', 'get_businesses'),
    (r'^businesses/query/(?P<oid>\d+)/$', 'query_businesses'),

    (r'^business/(?P<oid>\d+)/$', 'get_business'),
    (r'^business/add/$', 'add_business'),
    (r'^business/remove/(?P<oid>\d+)/$', 'remove_business'),
    (r'^business/edit/(?P<oid>\d+)/$', 'edit_business'),
    (r'^business/rate/(?P<oid>\d+)/$', 'rate_business'),
    
    #returns the categories associated  with a business
    (r'^business/categories/(?P<oid>\d+)/$', 'get_business_categories'),
    (r'^business/category/(?P<oid>\d+)/$', 'get_business_category'),
    (r'^business/category/add/$', 'add_business_category'),
    (r'^business/category/remove/(?P<oid>\d+)/$', 'remove_business_category'),
    (r'^business/category/rate/(?P<oid>\d+)/$', 'rate_business_category'),
    (r'^tags/$', 'get_tags'),


   #currently not designed / implemented    
   # (r'^comments/$', 'get_comment'),
    (r'^comment/(?P<oid>\d+)/$', 'get_comment'),
    (r'^comment/add/$', 'add_comment'),
    (r'^comment/remove/$', 'remove_comment'),
    (r'^comment/rate/(?P<oid>\d+)/$', 'rate_comment'),
    (r'^comment/edit/(?P<oid>\d+)/$','edit_comment'),
    
    (r'^photos/(?P<oid>\d+)/$', 'get_photos'),
    (r'^photo/(?P<oid>\d+)/$', 'get_photo'),
    (r'^photo/add/$', 'add_photo'),
    (r'^photo/remove/(?P<oid>\d+)/$', 'remove_photo'),
    (r'^photo/rate/(?P<oid>\d+)/$', 'rate_photo'),

    (r'^queries/$', 'get_queries'),
    (r'^query/(?P<oid>\d+)/$', 'get_query'),
    (r'^query/remove/(?P<oid>\d+)/$', 'get_query'),
    (r'^query/add/$', 'add_query'),
    (r'^query/edit/(?P<oid>\d+)/$', 'edit_query')




)

