'''
Created on May 17, 2012

@author: zouf
'''
from ratings.models import Rating

#Files for miscellaneous database accesses

def getNumRatings(business):
    ratset = Rating.objects.filter(business=business)
    return ratset.count()
