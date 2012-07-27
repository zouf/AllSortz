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
def get_bus_data_ios(business_list, user):
    data = []
    for b in business_list:
        d = get_single_bus_data_ios(b, user)
        data.append(d)
    return data


#isSideBar is true if we're using small images
def get_single_bus_data_ios(b, user):
    if b.lat == 0 or b.lon == 0:
        b = setBusLatLng(b)

    d = dict()
    d['name'] = b.name
    d['city'] = b.city
    d['state'] = b.state
    d['address'] = b.address
    d['latitude'] = b.lat
    d['longitude'] = b.lon
    d['businessID'] = b.id


    d['distanceFromCurrentUser'] = b.dist


    d['ratingOverAllUsers']  = round(getBusAvg(b.id) * 2) / 2
    d['photo'] = get_photo_thumb_url(b)
    d['numberOfRatings'] = getNumRatings(b.id)

    d['numberOfLoves'] = getNumLoved(b)
    d['numberOfLikes'] = getNumLiked(b)

    #the user exists and has rated something
    if user and Rating.objects.filter(user=user, business=b).count() > 0:
        r = Rating.objects.get(user=user, business=b)
        d['this_rat'] = r.rating
        d['ratingForCurrentUser'] = r.rating
    else:
        d['this_rat'] = 0
        d['ratingForCurrentUser'] = 0

    bustags = BusinessTag.objects.filter(business=b).exclude(tag=get_master_summary_tag())
    d['tags'] = []
    for bt in bustags:

        if not is_master_summary_tag(bt.tag):
            tagDict = dict()
            tagDict['name'] = bt.tag.descr
            tagDict['id'] = bt.tag.id
            d['tags'].append(tagDict)


    if d['rating'] == 0:
        #b.recommendation = get_best_current_recommendation(b, user)

        d['ratingRecommendation'] = getBusAvg(b.id)
    return d
