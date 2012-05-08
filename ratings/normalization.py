'''
Created on May 8, 2012

@author: zouf
'''
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum, Count
from ratings.models import Business, Rating, UserMeta
import math

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
        avg = ci_lowerbound(sumRating, countRating)
        b = Business.objects.get( id=bus.id)
        b.average_rating = avg
        b.save()
    usermeta = []
    for user in User.objects.all():
        ratingFilter = Rating.objects.filter(username=user).aggregate(Sum('rating'), Count('rating'))
        sumRating = ratingFilter['rating__sum']
        countRating = ratingFilter['rating__count']
        avg = ci_lowerbound(sumRating,countRating)
        meta = UserMeta(average_rating=avg, user=user)
        usermeta.append(meta)
    UserMeta.objects.bulk_create(usermeta)


def getBusAvg(bid):
    b = Business.objects.get(id=bid)
    return b.average_rating

def getUserAvg(uid):
    u = User.objects.get(id=uid)
    return u.average_rating

def getNormFactors(uid,bid):
    glb = getGlobalAverage()
    usr = getUserAvg(uid)
    bus = getBusAvg(bid)
    return (glb + usr + bus)

def getGlobalAverage():
    res = Rating.objects.all().aggregate(Sum('rating'),Count('rating'))
    return res['rating__sum']/res['rating__count']
