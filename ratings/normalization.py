'''
Created on May 8, 2012

@author: zouf
'''
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum, Count
from numpy.ma.core import std
from ratings.models import Business, Rating, UserMeta
import math
import numpy

def calcStdev():
    businesses = Business.objects.all()
    bList = []
    for b in businesses:
        bList.append(b.average_rating)

    users = UserMeta.objects.all()
    uList = []
    for u in users:
        uList.append(u.average_rating)
    
    stdevAllRat = std(bList)
    stdevURat = std(uList)
    return float(stdevURat**2)/float(stdevAllRat**2)
                       
                       
#from http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
def ci_lowerbound(numPosRev, numTotalRev):
    z = 1.96 #for confidence of 0.95
    if numTotalRev == 0:
        return 0
    p_hat = 1.0 * numPosRev / numTotalRev
    return(p_hat + z * z / (2 * numTotalRev) - z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * numTotalRev) / numTotalRev) / (1 + z * z / numTotalRev)))

def buildAverageRatings():
    all_businesses = Business.objects.all()
    for bus in all_businesses:
        ratingFilter = Rating.objects.filter(business=bus).aggregate(Sum('rating'), Count('rating'))
        sumRating = ratingFilter['rating__sum']
        countRating = ratingFilter['rating__count']
        if countRating == 0:
          avg = 0
        else:
          avg = float(float(sumRating) / float(countRating)) #ci_lowerbound(sumRating,countRating)
        b = Business.objects.get( id=bus.id)
        print('sum rat is ' + str(sumRating))
        print('count rat is ' + str(countRating))
        print(' avg is ' + str(avg))
        b.average_rating = avg
        b.save()
    usermeta = []
    UserMeta.objects.all().delete()
    for user in User.objects.all():
        ratingFilter = Rating.objects.filter(username=user).aggregate(Sum('rating'), Count('rating'))
        sumRating = ratingFilter['rating__sum']
        countRating = ratingFilter['rating__count']
        if countRating == 0:
          avg = 0
        else:
          avg = float(float(sumRating) / float(countRating)) #ci_lowerbound(sumRating,countRating)
        print('sum rat is ' + str(sumRating))
        print('count rat is ' + str(countRating))
        print(' avg is ' + str(avg))

        
        meta = UserMeta(average_rating=avg, user=user)
        usermeta.append(meta)
    UserMeta.objects.bulk_create(usermeta)


def getBusAvg(bid):
    ratingFilter = Rating.objects.filter(business=Business.objects.get(id=bid)).aggregate(Sum('rating'), Count('rating'))
    sumRating = ratingFilter['rating__sum']
    countRating = ratingFilter['rating__count']
    avg = 0
    K = 5#calcStdev()
    if countRating != 0:
      glb = getGlobalAverage()
      avg = (glb * K + float(sumRating)) / (K + float(countRating)) #ci_lowerbound(sumRating,countRating)
    return avg
    #b = Business.objects.get(id=bid)
    #return b.average_rating

def getUserAvg(uid):
    ratingFilter = Rating.objects.filter(username=User.objects.get(id=uid)).aggregate(Sum('rating'), Count('rating'))
    sumRating = ratingFilter['rating__sum']
    countRating = ratingFilter['rating__count']
    avg = 0
    K = 5#calcStdev()
    if countRating != 0:
      glb = getGlobalAverage()
      avg = (float(glb * K) + float(sumRating)) / (float(K) + float(countRating)) #ci_lowerbound(sumRating,countRating)
    return avg
    #u = UserMeta.objects.get(user=User.objects.get(id=uid))
    #return u.average_rating

def getNormFactors(uid,bid):
    glb = getGlobalAverage()
    usr = getUserAvg(uid)
    bus = getBusAvg(bid)
    fct = (usr + bus - glb)
    return(fct)

def getGlobalAverage():
    res = Rating.objects.all().aggregate(Sum('rating'),Count('rating'))
    return (float(res['rating__sum'])/float(res['rating__count']))
