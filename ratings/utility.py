'''
Created on May 17, 2012

@author: zouf
'''

from communities.models import BusinessMembership
from communities.views import get_community
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.encoding import smart_str
from photos.views import get_photo_mini_url, get_photo_web_url, \
    get_photo_thumb_url
from ratings.favorite import get_user_favorites
from ratings.models import Rating, Business
from recommendation.normalization import getNumPosRatings, getNumNegRatings, \
    getBusAvg, getNumLoved, getNumLiked
from tags.models import BusinessTag
import logging
import simplejson
import time
import urllib
import urllib2


#from rateout.settings import LOG_FILE
#import time

logger = logging.getLogger(__name__)

def convertAddressToLatLng():
    for b in Business.objects.all():
        loc = b.address + " " + b.city + ", " + b.state
        i = 0
        time.sleep(5)
        latlng = get_lat(loc)
        if latlng:
            b.lat = latlng[0]
            b.lon = latlng[1]
            b.save()

#isSideBar is true if we're using small images
def get_single_bus_data(b,user,isSideBar=False):
    b.average_rating = round(getBusAvg(b.id) * 2) / 2

    if isSideBar:
        b.photourl = get_photo_thumb_url(b)
    else:
        b.photourl = get_photo_web_url(b)
    
    
    b.num_ratings = getNumRatings(b.id)
    



    b.loved = getNumLoved(b)
    b.liked = getNumLiked(b)
    thisRat = Rating.objects.filter(user=user, business=b)
    if thisRat.count() > 0:
        r = Rating.objects.get(user=user, business=b)
        b.this_rat = r.rating
        b.rating = r.rating
    else:
        b.this_rat = 0
        b.rating = 0
        
    bustags = BusinessTag.objects.filter(business=b)
    b.tags = []
    for bt in bustags:
        b.tags.append(bt.tag)

    
    return b



#TODO: matt fix this to handle ratings from 1-4
#is SideBar is true if we're going to use smaller data 
def get_bus_data(business_list,user,isSideBar=True):
    for b in business_list:
        b = get_single_bus_data(b,user,isSideBar)
        
    return business_list





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



def paginate_businesses(business_list,page, num):
    paginator = Paginator(business_list, num)  # Show 25 contacts per page
    try:
        business_list = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        business_list = paginator.page(1)
    except EmptyPage:
        business_list = paginator.page(paginator.num_pages)
    return business_list


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
    print(businesses)
    business_list = get_bus_data(businesses,user,isSideBar)
    business_list = paginate_businesses(business_list,page,5)

    for b in business_list:
        bustags = BusinessTag.objects.filter(business=b)
        b.tags = []
        for bt in bustags:
            b.tags.append(bt.tag)
        
    return business_list

def get_businesses_trending(user,page,checkForIntersection,isSideBar=False):
    alreadyThere = dict()
    for nt in checkForIntersection:
        alreadyThere[nt] = True
        
    print('getting everything')
    businesses = []
    try:
        allBus = Business.objects.all() # order by rating
        for b in allBus:
            if b not in alreadyThere:
                businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    business_list = get_bus_data(businesses,user,isSideBar)
    #business_list = paginate_businesses(business_list,page,5)
    for b in business_list:
        bustags = BusinessTag.objects.filter(business=b)
        b.tags = []
        for bt in bustags:
            b.tags.append(bt.tag)
    return business_list
        
        
def get_businesses_by_your(user,page,checkForIntersection,isSideBar=False):
    alreadyThere = dict()
    for nt in checkForIntersection:
        alreadyThere[nt] = True
        
    businesses = []
    try:
        allBus = get_user_favorites(user) # order by rating
        for b in allBus:
            if b not in alreadyThere:
                businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    business_list = get_bus_data(businesses,user,isSideBar)
    business_list = paginate_businesses(business_list,page,5)
    return business_list


def get_businesses_by_tag(t,user,page):
    bustags = BusinessTag.objects.filter(tag=t)
    businesses = []
    for bt in bustags:
        businesses.append(bt.business)    
    business_list = get_bus_data(businesses,user)
    business_list = paginate_businesses(business_list,page,5)
    return business_list

        
