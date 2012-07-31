'''
Created on Jul 19, 2012

@author: zouf
'''
#from photos.models import BusinessPhoto

from ios_interface.photos import get_photo_url
from ratings.models import Rating, Business, PageRelationship
from ratings.utility import setBusLatLng
from recommendation.normalization import getBusAvg, getNumRatings, getNumLoved, \
    getNumLiked
from tags.models import BusinessTag
from tags.views import get_master_summary_tag, is_master_summary_tag
from ios_interface.serializer import get_category_data


#TODO: matt fix this to handle ratings from 1-4
#is SideBar is true if we're going to use smaller data
def get_bus_data_ios(business_list, user):
    data = []
    for b in business_list:
        d = get_single_bus_data_ios(b, user)
        data.append(d)
    return data

class ReadJSONError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

 
def get_json_post_or_error(key,request):
    if key in request.POST:
        return request.POST[key]
    raise ReadJSONError("POST Key: " + str(key) + " not found in request " + str(request.path))



def get_json_get_or_error(key,request):
    if key in request.GET:
        return request.GET[key]
    raise ReadJSONError("GET Key: '" + str(key) + "' not found in request " + str(request.path))



def get_all_nearby(mylat,mylng,distance=1):

    current_pg_point = "point '({:.5f}, {:.5f})'".format(mylng, mylat)
    buses_query = " ".join(["SELECT *",
                                    "FROM (SELECT id, (point(lon, lat) <@> {}) AS dist FROM ratings_business) AS dists",
                                    "WHERE dist <= {:4f} ORDER BY dist ASC;"]).format(current_pg_point, distance)
    buses = Business.objects.raw(buses_query)
    return buses


#isSideBar is true if we're using small images
def get_single_bus_data_ios(b, user):
    if b.lat == 0 or b.lon == 0:
        b = setBusLatLng(b)

    d = dict()
    d['businessID'] = b.id
    d['businessName'] = b.name
    d['businessCity'] = b.city
    d['businessState'] = b.state
    d['streetAddr'] = b.address

    d['latitude'] = b.lat
    d['longitude'] = b.lon
    d['businessID'] = b.id
    d['businessPhone'] = '555 555-5555'

    d['distanceFromCurrentUser'] = str(b.distance)


    d['ratingOverAllUsers']  = round(getBusAvg(b.id) * 2) / 2
    d['photo'] = get_photo_url(b)
    d['numberOfRatings'] = getNumRatings(b.id)

    d['numberOfLoves'] = getNumLoved(b)
    d['numberOfLikes'] = getNumLiked(b)

    #the user exists and has rated something
    if user and Rating.objects.filter(user=user, business=b).count() > 0:
        try:
            r = Rating.objects.get(user=user, business=b)
        except Rating.MultipleObjectsReturned:
            r = Rating.objects.filter(user=user,business=b)[0]
        d['ratingForCurrentUser'] = r.rating
    else:
        d['ratingForCurrentUser'] = 0

    bustags = BusinessTag.objects.filter(business=b)   #.exclude(tag=get_master_summary_tag())
    d['categories'] = []
    for bt in bustags:
        d['categories'].append(get_category_data(bt,user))


    if d['ratingForCurrentUser'] == 0:
        #b.recommendation = get_best_current_recommendation(b, user)

        d['ratingRecommendation'] = getBusAvg(b.id)
    return d
