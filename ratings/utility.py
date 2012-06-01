'''
Created on May 17, 2012

@author: zouf
'''
from django.utils.encoding import smart_str
from rateout.settings import LOG_FILE
from ratings.models import Rating
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
    print(ft)
    if ft["status"] == 'OK':
        lat = str(ft["results"][0]['geometry']['location']['lat']) 
        lng = str(ft["results"][0]['geometry']['location']['lng'])
        return [lat, lng]
    return False