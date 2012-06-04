'''
Created on May 17, 2012

@author: zouf
'''
from django.utils.encoding import smart_str
from rateout.settings import LOG_FILE
from ratings.models import Rating, BusinessPhoto
import simplejson
import time
import urllib
import urllib2

#Files for miscellaneous database accesses


def getNumRatings(business):
    ratset = Rating.objects.filter(business=business)
    return ratset.count()


def log_msg(msg):
    fp = open(LOG_FILE, "a")
    fp.write(time.asctime())
    fp.write(msg)
    print(msg)
    fp.write('\n')
    
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
    print(ph.url)
    return ph.url