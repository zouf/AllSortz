'''
Created on May 17, 2012

@author: zouf
'''

from django.utils.encoding import smart_str
from photos.views import get_photo_web_url, get_photo_thumb_url
from rateout.settings import FB_APP_SECRET
from ratings.models import Rating
from recommendation.normalization import getNumPosRatings, getNumNegRatings, \
    getBusAvg
from tags.models import BusinessTag
import base64
import hashlib
import hmac
import json
import logging
import simplejson
import urllib
import urllib2
#from rateout.settings import LOG_FILE
#import time

logger = logging.getLogger(__name__)


def get_single_bus_data(b,user):
    b.average_rating = round(getBusAvg(b.id) * 2) / 2
    b.photourl = get_photo_thumb_url(b)
    b.num_ratings = getNumRatings(b.id)
       
    latlng = get_lat(b.address + " " + b.city + ", " + b.state)
    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE

    if latlng:
        b.lat=latlng[0]
        b.lon = latlng[1]
    else:
        b.lat = 0
        b.lon = 0
    if user.is_authenticated():
        b.pos_ratings = getNumPosRatings(b)
        b.neg_ratings = getNumNegRatings(b)
        thisRat = Rating.objects.filter(username=user, business=b)
        if thisRat.count() > 0:
            r = Rating.objects.get(username=user, business=b)
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
def get_bus_data(business_list,user):
    for b in business_list:
        b = get_single_bus_data(b,user)
        
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
    if ft["status"] == 'OK':
        lat = str(ft["results"][0]['geometry']['location']['lat']) 
        lng = str(ft["results"][0]['geometry']['location']['lng'])
        return [lat, lng]
    return False

