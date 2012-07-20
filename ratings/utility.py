'''
Created on May 17, 2012

@author: zouf
'''

from allsortz.search import get_all_nearby
from communities.models import BusinessMembership
from communities.views import get_community
from django.utils.encoding import smart_str
from geopy import geocoders
from photos.views import get_photo_web_url, get_photo_thumb_url
from ratings.favorite import get_user_favorites
from ratings.models import Rating, Business
from recommendation.normalization import getBusAvg, getNumLoved, getNumLiked
from recommendation.recengine import get_best_current_recommendation
from tags.models import BusinessTag
from tags.views import get_master_summary_tag, is_master_summary_tag, \
    get_master_page_business
import logging
import simplejson
import time
import urllib
import urllib2


DEFAULT_DISTANCE =3 
#from rateout.settings import LOG_FILE
#import time

logger = logging.getLogger(__name__)

def setBusLatLng(b):
    if b.lat == 0 or b.long == 0:
        loc = b.address + " " + b.city + ", " + b.state
        latlng = get_lat(loc)
        b.lat = latlng[0]
        b.lon = latlng[1]
        b.save()
    return b
        

def convertAddressToLatLng():
    for b in Business.objects.all():
        setBusLatLng(b) 
        time.sleep(1)



#isSideBar is true if we're using small images
def get_single_bus_data(b,user,isSideBar=False):
    if b.lat == 0 or b.lon == 0:
        b = setBusLatLng(b)
    
    b.average_rating = round(getBusAvg(b.id) * 2) / 2

    if isSideBar:
        b.photourl = get_photo_thumb_url(b)
    else:
        b.photourl = get_photo_web_url(b)
    
    
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
        b.recommendation = int(round(getBusAvg(b.id)))
    else:
        b.recommendation = 0
    b.master_page = get_master_page_business(b)
    return b



#TODO: matt fix this to handle ratings from 1-4
#is SideBar is true if we're going to use smaller data 
def  get_bus_data(business_list,user,isSideBar=True):
    return_list = []
    for b in business_list:
        bus = Business.objects.get(id=b.id)
        bus = get_single_bus_data(bus,user,isSideBar)
        #user has been here before
        
        if bus.recommendation > 0: 
            bus.weight = b.dist + bus.recommendation 
        else:
            bus.weight = b.dist + bus.rating 
        bus.dist = b.dist
        return_list.append(bus)
    return return_list





def getNumRatings(business):
    ratset = Rating.objects.filter(business=business)
    return ratset.count()


#returns the average latitude and longitude
def get_avg_latlng(business_list):
    latsum = 0
    lonsum = 0
        
    for b in business_list:
        latsum += float(b.lat)
        lonsum += float(b.lon)
    return [latsum / len(business_list),lonsum / len(business_list) ]    



#from 
#http://djangosnippets.org/snippets/2399/
def get_lat(loc):
    location = urllib.quote_plus(smart_str(loc))
    dd = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % location).read() 
    ft = simplejson.loads(dd)
    print(ft)
    if ft["status"] == 'OK':
        lat = str(ft["results"][0]['geometry']['location']['lat']) 
        lng = str(ft["results"][0]['geometry']['location']['lng'])
        return [lat, lng]
    return None



#def paginate_businesses(business_list,page, num):
#    paginator = Paginator(business_list, num)  # Show 25 contacts per page
#    try:
#        business_list = paginator.page(page)
#    except (PageNotAnInteger, TypeError):
#        business_list = paginator.page(1)
#    except EmptyPage:
#        business_list = paginator.page(paginator.num_pages)
#    return business_list


def get_businesses_by_community(user,page,checkForIntersection,isSideBar=False):
    alreadyThere = dict()
    for nt in checkForIntersection:
        alreadyThere[nt] = True
    community = get_community(user)
    businesses = []
    try:
        busMembership = BusinessMembership.objects.filter(community = community)

        for b in busMembership:
            if b not in alreadyThere:
                businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    business_list = get_bus_data(businesses,user,isSideBar)


    return business_list


def sort_weight(b1,b2):
    return cmp(b2.weight, b1.weight)
    



def get_top_unvisited_businesses(user,page,checkForIntersection,isSideBar=False):

    alreadyThere = dict()
#    for nt in checkForIntersection:
#        alreadyThere[nt] = True
#        
#    businesses = []
#    try:
#        allBus = Business.objects.all() # order by rating
#        for b in allBus:
#            if b not in alreadyThere:
#                businesses.append(b.business)
#    except:
#        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
#        businesses = Business.objects.all()
    
    g = geocoders.Google()
    place, (lat, lng) = g.geocode("Princeton, NJ")  
    
    #search around princeton
    business_list = get_bus_data(get_all_nearby(lat,lng,DEFAULT_DISTANCE),user,isSideBar)
    business_list = sorted(business_list,cmp=sort_weight)
    final_list = []
    for b in business_list:
        

        
        if b.recommendation > 0:
            print('rec is ' + str(b.recommendation))
            print('rat is ' + str(b.rating))
            final_list.append(b)
    
    return final_list
        
        
def get_businesses_by_your(user,page,checkForIntersection,isSideBar=False):
#    alreadyThere = dict()
#    for nt in checkForIntersection:
#        alreadyThere[nt] = True
        
    businesses = []
#    try:
#        allBus = get_user_favorites(user) # order by rating
#        for b in allBus:
#            if b not in alreadyThere:
#                businesses.append(b.business)
#    except:
#        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
#        businesses = Business.objects.all()
    g = geocoders.Google()
    place, (lat, lng) = g.geocode("Princeton, NJ")  
    business_list = get_bus_data(get_all_nearby(lat, lng, DEFAULT_DISTANCE),user,isSideBar)
    final_list = []
    for b in business_list:
        if b.rating > 0:
            print('orec is ' + str(b.recommendation))
            print('orat is ' + str(b.rating)+'\n')
            final_list.append(b)

    return final_list


def get_businesses_by_tag(t,user,page):
    bustags = BusinessTag.objects.filter(tag=t)
    businesses = []
    for bt in bustags:
        businesses.append(bt.business)    
    business_list = get_bus_data(businesses,user)
    return business_list

        
