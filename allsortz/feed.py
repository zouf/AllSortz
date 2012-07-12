'''
Created on Jul 11, 2012

@author: zouf
'''
from comments.models import BusinessComment, Comment, TagComment
from ratings.models import Rating
from ratings.utility import get_single_bus_data


def get_bus_recent_activity(b):
    ratings = Rating.objects.filter(business=b).order_by('-date')[:5]
   
    feed = []
    
    for r in ratings:
        r.type = "business"
        feed.append(r)
    allbuscomments = BusinessComment.objects.filter(business=b).order_by('-date')
    for c in allbuscomments:  
        bc = c
        bc.type = "buscomment"
        feed.append(bc)
    return feed
    
    



def get_user_recent_activity(user):
 
    ratings = Rating.objects.filter(user=user).order_by('-date')[:5]
   
    feed = []
    
    for r in ratings:
        r.type = "business"
        r.business = get_single_bus_data(r.business, user, isSideBar=True)
        feed.append(r)
    allcomments = Comment.objects.filter(user=user).order_by('-date')
    for c in allcomments:
        try: 
            tc = TagComment.objects.get(thread=c)
            tc.type = "tagcomment"
            tc.business = get_single_bus_data(tc.business, user, isSideBar=True)
            feed.append(tc)
        except:
            pass
        
        try:
            bc = BusinessComment.objects.get(thread=c)
            bc.business = get_single_bus_data(bc.business, user, isSideBar=True)
            bc.type = "buscomment"
            feed.append(bc)
        except:
            pass
    return feed
    
    
    
    

def get_all_recent_activity():
 
    ratings = Rating.objects.filter().order_by('-date')[:5]
   
    feed = []
    
    for r in ratings:
        r.type = "business"
        r.business = get_single_bus_data(r.business, r.user, isSideBar=True)
        feed.append(r)
    allcomments = Comment.objects.filter().order_by('-date')
    for c in allcomments:
        try: 
            tc = TagComment.objects.get(thread=c)
            tc.type = "tagcomment"
            tc.business = get_single_bus_data(tc.business, c.user, isSideBar=True)
            tc.user = c.user
            feed.append(tc)
        except:
            pass
        
        try:
            bc = BusinessComment.objects.get(thread=c)
            bc.business = get_single_bus_data(bc.business, c.user, isSideBar=True)
            bc.type = "buscomment"
            bc.user = c.user
            feed.append(bc)
        except:
            pass
    return feed
    