'''
Created on May 17, 2012

@author: zouf
'''
from django.utils.encoding import smart_str
from ratings.models import Rating, BusinessPhoto, Tip, TipRating, Tag, TagRating
from recommendation.normalization import getNumPosRatings, getNumNegRatings, \
    getBusAvg
import logging
import simplejson
import urllib
import urllib2
#from rateout.settings import LOG_FILE
#import time

logger = logging.getLogger(__name__)



def get_bus_data(business_list,user):
    for b in business_list:
        b.average_rating = round(getBusAvg(b.id) * 2) / 2
    
        b.num_ratings = getNumRatings(b.id)
        if user.is_authenticated():
            b.pos_ratings = getNumPosRatings(b)
            b.neg_ratings = getNumNegRatings(b)
            thisRat = Rating.objects.filter(username=user, business=b)
            if thisRat.count() > 0:
                r = Rating.objects.get(username=user, business=b)
                b.this_rat = r.rating
            else:
                b.this_rat = 0
    return business_list





def getNumRatings(business):
    ratset = Rating.objects.filter(business=business)
    return ratset.count()



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

#for businesses
def get_photo_thumb_url(b):
    qset  = BusinessPhoto.objects.filter(business=b)
    if qset.count < 1:
        return False
    ph = qset[0].image_thumb
    return ph.url