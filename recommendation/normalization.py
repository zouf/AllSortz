'''
Created on May 8, 2012

@author: zouf
'''
from activities.models import ActRating
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum, Count
from ios_interface.models import PhotoRating, DiscussionRating
from ratings.models import Rating, Business, CommentRating
from tags.models import TagRating
import math


def isTagRelevant(bt):
    numPos = getNumPosRatings(bt)
    numNeg = getNumNegRatings(bt)
    if numPos < numNeg and numNeg > 1:
        return False
    return True


def getNumLiked(bus):
    ratingFilter = Rating.objects.filter(business=bus, rating__range=["3", "3"])
    ratingFilter = ratingFilter.aggregate(Count('rating'))
    countRating = ratingFilter['rating__count']
    return countRating


def getNumLoved(bus):
    ratingFilter = Rating.objects.filter(business=bus, rating__range=["4", "4"])
    ratingFilter = ratingFilter.aggregate(Count('rating'))
    countRating = ratingFilter['rating__count']
    return countRating

def getNumDisliked(bus):
    ratingFilter = Rating.objects.filter(business=bus, rating__range=["2", "2"])
    ratingFilter = ratingFilter.aggregate(Count('rating'))
    countRating = ratingFilter['rating__count']
    return countRating

def getNumHated(bus):
    ratingFilter = Rating.objects.filter(business=bus, rating__range=["1", "1"])
    ratingFilter = ratingFilter.aggregate(Count('rating'))
    countRating = ratingFilter['rating__count']
    return countRating



def getNumPosRatings(o):
    #get class name
    t = o.__class__.__name__
    if t == "Business":
        ratingFilter = Rating.objects.filter(business=o, rating__range=["3", "5"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t == 'Discussion':
        ratingFilter = DiscussionRating.objects.filter(discussion=o, rating__range=["1", "5"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t == 'Comment':
        ratingFilter = CommentRating.objects.filter(comment=o, rating__range=["1", "5"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t == 'Photo':
        ratingFilter = PhotoRating.objects.filter(photo=o, rating__range=["1", "5"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t=="Activity":
        ratingFilter = ActRating.objects.filter(activity=o,rating__range=["3", "5"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t == 'BusinessTag':
        ratingFilter = TagRating.objects.filter(tag=o, rating__range=["3", "5"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    else:
        print("error in getnumpos")


def getNumNegRatings(o):
    t = o.__class__.__name__
    if t == 'Business':
        ratingFilter = Rating.objects.filter(business=o, rating__range=["1", "2"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t == 'Comment':
        ratingFilter = DiscussionRating.objects.filter(discussion=o, rating=0)
        countRating = ratingFilter.count()
        return countRating
    #TODO: transition the comments to be 0=> neg, 1=>positive
    elif t == 'Comment':
        ratingFilter = CommentRating.objects.filter(comment=o, rating=0)
        countRating = ratingFilter.count()
        return countRating
    elif t == 'Photo':
        ratingFilter = PhotoRating.objects.filter(photo=o, rating=0)
        countRating = ratingFilter.count()
        return countRating
    elif t=="Activity":
        ratingFilter = ActRating.objects.filter(activity=o,rating__range=["1", "2"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    elif t == 'BusinessTag':
        ratingFilter = TagRating.objects.filter(tag=o, rating__range=["1", "2"])
        ratingFilter = ratingFilter.aggregate(Count('rating'))
        countRating = ratingFilter['rating__count']
        return countRating
    else:
        print("error in getnumneg")


def calcStdev():
    businesses = Business.objects.all()
    bList = []
    for b in businesses:
        bList.append(b.average_rating)

    #users = UserMeta.objects.all()
    uList = []
    for u in User.objects.all():
        uList.append(getUserAvg(u.id))

    stdevAllRat = 0#std(bList)
    stdevURat =0# std(uList)
    return float(stdevURat ** 2) / float(stdevAllRat ** 2)


#from http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
def ci_lowerbound(numPosRev, numTotalRev):
    z = 1.96  # for confidence of 0.95
    if numTotalRev == 0:
        return 0
    p_hat = 1.0 * numPosRev / numTotalRev
    return(p_hat + z * z / (2 * numTotalRev) - z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * numTotalRev) / numTotalRev) / (1 + z * z / numTotalRev)))

#def buildAverageRatings():
#       all_businesses = Business.objects.all()
#       for bus in all_businesses:
#               ratingFilter = Rating.objects.filter(business=bus).aggregate(Sum('rating'), Count('rating'))
#               sumRating = ratingFilter['rating__sum']
#               countRating = ratingFilter['rating__count']
#               if countRating == 0:
#                 avg = 0
#               else:
#                 avg = float(float(sumRating) / float(countRating)) #ci_lowerbound(sumRating,countRating)
#               b = Business.objects.get( id=bus.id)
#               #print('sum rat is ' + str(sumRating))
#               #print('count rat is ' + str(countRating))
#               #print(' avg is ' + str(avg))
#               b.average_rating = avg
#               b.save()
#       usermeta = []
#       UserMeta.objects.all().delete()
#       for user in User.objects.all():
#               ratingFilter = Rating.objects.filter(username=user).aggregate(Sum('rating'), Count('rating'))
#               sumRating = ratingFilter['rating__sum']
#               countRating = ratingFilter['rating__count']
#               if countRating == 0:
#                 avg = 0
#               else:
#                 avg = float(float(sumRating) / float(countRating)) #ci_lowerbound(sumRating,countRating)
#               #print('sum rat is ' + str(sumRating))
#               #print('count rat is ' + str(countRating))
#               #print(' avg is ' + str(avg))
#
#
#               meta = UserMeta(average_rating=avg, user=user)
#               usermeta.append(meta)
#       UserMeta.objects.bulk_create(usermeta)


def getBusAvg(bid):
    #       if bid in businessCache:
    #         return businessCache[bid]
    ratingFilter = Rating.objects.filter(business=Business.objects.get(id=bid)).aggregate(Sum('rating'), Count('rating'))
    sumRating = ratingFilter['rating__sum']
    countRating = ratingFilter['rating__count']

    avg = 0
    K = 5  # calcStdev()
    if countRating != 0:
        glb = getGlobalAverage()
        avg = (glb * K + float(sumRating)) / (K + float(countRating))  # ci_lowerbound(sumRating,countRating)
    #       businessCache[bid] = avg
    return avg
    #b = Business.objects.get(id=bid)
    #return b.average_rating


def getUserAvg(uid):
    ratingFilter = Rating.objects.filter(user=User.objects.get(id=uid)).aggregate(Sum('rating'), Count('rating'))
    sumRating = ratingFilter['rating__sum']
    countRating = ratingFilter['rating__count']
    avg = 0
    K = 5  # calcStdev()
    if countRating != 0:
        glb = getGlobalAverage()
        avg = (float(glb * K) + float(sumRating)) / (float(K) + float(countRating))  # ci_lowerbound(sumRating,countRating)
    #       userCache[uid] = avg
    return avg
    #u = UserMeta.objects.get(user=User.objects.get(id=uid))
    #return u.average_rating


def getNormFactors(uid, bid):
    glb = getGlobalAverage()
    usr = getUserAvg(uid)
    bus = getBusAvg(bid)
    fct = (usr + bus - glb)
    return(fct)


def getNumRatings(bid):
    ratingFilter = Rating.objects.filter(business=Business.objects.get(id=bid)).aggregate(Sum('rating'), Count('rating'))
    countRating = ratingFilter['rating__count']
    return countRating


def getGlobalAverage():
    res = Rating.objects.all().aggregate(Sum('rating'), Count('rating'))
    count = res['rating__count']
    if count != 0:
        return (float(res['rating__sum']) / float(res['rating__count']))
    return 0
