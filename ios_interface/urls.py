from django.conf.urls import patterns

urlpatterns = patterns('ios_interface.views',
    (r'^businesses/$', 'get_businesses'),
    (r'^business/$', 'get_business'),
    (r'^business/rate/$', 'rate_business'),
    
    #returns the categories associated  with a business
    (r'^business/categories/$', 'get_business_categories'),
    (r'^business/category/$', 'get_business_category'),
    (r'^business/category/rate/$', 'rate_business_category'),

   #currently not designed / implemented    
   # (r'^comments/$', 'get_comment'),
    (r'^comment/$', 'get_comment'),
    (r'^comment/rate/$', 'rate_comment'),
    
    (r'^photos/$', 'get_photos'),
    (r'^photo/$', 'get_photo'),
    (r'^photo/rate/$', 'rate_photo'),

    (r'^queries/$', 'get_queries'),
    (r'^query/$', 'get_query')  

)

