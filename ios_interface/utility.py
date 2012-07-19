'''
Created on Jul 19, 2012

@author: zouf
'''
from photos.views import get_photo_thumb_url
from ratings.models import Rating
from ratings.utility import setBusLatLng
from recommendation.normalization import getBusAvg, getNumRatings, getNumLoved, \
    getNumLiked
from tags.models import BusinessTag
from tags.views import get_master_summary_tag, is_master_summary_tag

#TODO: matt fix this to handle ratings from 1-4
#is SideBar is true if we're going to use smaller data 
def  get_bus_data_ios(business_list,user):
    for b in business_list:
        b = get_single_bus_data_ios(b,user)
    return business_list


#isSideBar is true if we're using small images
def get_single_bus_data_ios(b,user):
    if b.lat == 0 or b.lon == 0:
        b = setBusLatLng(b)
    
    b.average_rating = round(getBusAvg(b.id) * 2) / 2
    b.photourl = get_photo_thumb_url(b)   
    b.num_ratings = getNumRatings(b.id)
    
    b.loved = getNumLoved(b)
    b.liked = getNumLiked(b)
    
    #the user exists and has rated something
    if user and  Rating.objects.filter(user=user, business=b).count() > 0:
        r = Rating.objects.get(user=user, business=b)
        b.this_rat = r.rating
        b.rating = r.rating
    else:
        b.this_rat = 0
        b.rating = 0
        
    bustags = BusinessTag.objects.filter(business=b).exclude(tag=get_master_summary_tag())
    b.tags = []
    for bt in bustags:
        if not is_master_summary_tag(bt.tag):
            b.tags.append(bt.tag)
            
    if b.rating == 0:
        #b.recommendation = get_best_current_recommendation(b,user)
        
        b.recommendation = getBusAvg(b.id)
    return b