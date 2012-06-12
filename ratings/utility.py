'''
Created on May 17, 2012

@author: zouf
'''
from django.utils.encoding import smart_str
from ratings.models import Rating, BusinessPhoto, Tip, TipRating, Tag, TagRating
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import logging
import simplejson
import urllib
import urllib2
#from rateout.settings import LOG_FILE
#import time

logger = logging.getLogger(__name__)

#Files for miscellaneous database accesses
def tiptag_comp(x,y):
    #eventually do something more intelligent here!
    xTot = x.pos_ratings - x.neg_ratings
    yTot = y.pos_ratings - y.neg_ratings
    if (xTot > yTot):
        return -1
    elif (xTot < yTot ):
        return 1
    else:
        return 0
    

def get_tips(b,user=False,q=""):
    if q != "":
        tips = Tip.objects.filter(descr__icontains=q)[:20]
    else:
        tips = Tip.objects.filter(business=b).order_by('-date')
    results = []
    for t in tips:
        try:
            rat =  TipRating.objects.get(tip=t)
            t.this_rat = rat.rating
            t.pos_ratings = getNumPosRatings(t)
            t.neg_ratings = getNumNegRatings(t)
        except:
            t.this_rat = 0
            t.pos_ratings = 0
            t.neg_ratings = 0
        results.append(t)

    #results.sort(cmp=tiptag_comp)
    return results
        


def get_tags(b,user=False,q=""):
    if q != "":
        tags = Tag.objects.filter(descr__icontains=q)[:20]
    else:
        tags = Tag.objects.filter(business=b).order_by('-date')
    results = []
    for t in tags:
        try:
            rat =  TagRating.objects.get(tag=t)
            t.this_rat = rat.rating
            t.pos_ratings = getNumPosRatings(t)
            t.neg_ratings = getNumNegRatings(t)
        except:
            t.this_rat = 0
            t.pos_ratings = 0
            t.neg_ratings = 0
        results.append(t)
    # results.sort(cmp=tiptag_comp)
    return results

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