from celery.decorators import task
import logging
import math
import random
import scipy
from scipy.stats.stats import pearsonr
from celery.decorators import periodic_task
from datetime import timedelta
from ratings.models import Business
from ratings.models import Rating
from ratings.models import Recommendation
from django.contrib.auth.models import User



import ratings.recengine



def get_rating_table_working_copy():
    ratingTable = dict()
    allBusinesses = Business.objects.all()
    allUsers = User.objects.all()
    
    for u in allUsers:
        ratingTable[u] = {}
        for b in allBusinesses:
            r = Rating.objects.filter(username=u, business=b)
            if r:
                r = Rating.objects.get(username=u, business=b)
                ratingTable[u][b] = r.rating
            else:
                ratingTable[u][b] = 0
    return ratingTable

def get_listof_most_similar_users(ratingTable, user):
    thisUserRatings = scipy.zeros(len(ratingTable[user]), float)
    j = 0
    # For some reason, I could not get append to work
    for r in ratingTable[user]:
        thisUserRatings[j] = float(ratingTable[user][r])
        j = j + 1
    
    correlationArray = {}
    for key, ratarr in ratingTable.iteritems():     # iterate through all ratings in teh array
        if key != user:                            #except for the users
            newArr = scipy.zeros(len(ratingTable[key]), float)
            i = 0
            for r in ratingTable[key]:
                newArr[i] = float(ratingTable[key][r])
                i = i + 1
            correlation = pearsonr(newArr, thisUserRatings)[0]
            print correlation
            if math.isnan(correlation):
                correlation = 0
            correlationArray[key] = correlation
    correlationArraySorted = sorted(correlationArray.iteritems(), key=lambda (k,v): (v,k))
    return correlationArraySorted

def calculate_recommendation(user, correlatedUsers, ratingTable):
    return 1


@periodic_task(name="tasks.build_recommendations", run_every = timedelta(seconds=10))
def build_recommendations():
    corArr = dict()
    ratingTable = get_rating_table_working_copy()
    for user in ratingTable:    
        corArr[user] = get_listof_most_similar_users(ratingTable, user)
    for user in corArr:
        for bus in ratingTable[user]:
            rec = calculate_recommendation(user,corArr, ratingTable)
            queryset = Recommendation.objects.filter(username=user, business=bus)
            if queryset.count() >= 1:
                queryset.delete()
            r1 = Recommendation(username=user, business=bus,recommendation=rec)
            r1.save()

                
    
            
            
    
            