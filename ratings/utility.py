'''
Created on May 17, 2012

@author: zouf
'''
from rateout.settings import LOG_FILE
from ratings.models import Rating
import time

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
