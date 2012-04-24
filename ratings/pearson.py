'''
Created on Apr 24, 2012

@author: zouf
'''
from ratings.tasks import  get_rating_table_working_copy
from ratings.tasks import  insertAverage
from ratings.tasks import  insertRecommendation
from ratings.models import Business
from ratings.models import User
from ratings.models import Rating
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Sum

import scipy
import numpy
import math
from scipy.stats.stats import pearsonr


corPositiveBound = 0.5
corNegativeBound = -0.5

def get_listof_most_similar_users(ratingTable, thisUser):
    #an array of correlations indexed by "other users
    correlationArray = {}
    
    #iterate through all other users
    for otherUser, ratingArr in ratingTable.iteritems():     
        thisUserOverlapRatings = []
        otherUserOverlapRatings = []
        if otherUser != thisUser:            #except for the current user
            #Get all the businesses and ratings of the other user
            for business, otherUserRating in ratingArr:
                thisUserRating = ratingTable[thisUser][business]
                #only use ratings both users have rated
                if otherUserRating >=0 and thisUserRating >= 0:
                    #for later conversion to scipy.array
                    thisUserOverlapRatings.append(thisUserRating)
                    otherUserOverlapRatings.append(otherUserRating)
        ratings1 = scipy.array(thisUserOverlapRatings)
        ratings2 = scipy.array(otherUserOverlapRatings)
        
        #ratings1 and ratings2 are arrays of floats which represent ratings for businesses
        # both this user and otherUser have rated
        correlation = pearsonr(ratings1, ratings2)[0]
        
        #since stdev can be 0
        if math.isnan(correlation):
            correlation = 0
        correlationArray[otherUser] = correlation
    correlationArraySorted = sorted(correlationArray.iteritems(), key=lambda (k, v): (v, k))
    return correlationArraySorted

    


#Given a corValue, is it big or small enough to matter
def sufficiently_correlated(corValue):
    global corNegativeBound
    global corPositiveBound
    if corValue >= corPositiveBound or corValue <= corNegativeBound:
        return True
    return False



        
def calculate_recommendation_allbusinesses(user, corUser, corValue, ratingTable, recArr):
    global g_NegR
    global g_PosR
    global g_NeuR
    global g_NoR
    for bus in ratingTable[corUser]: #go through all of the correlated user's businesses
        print("Iterate over businesses for "+corUser.username+ " w.r.t. "+user.username)
        if ratingTable[user][bus] == g_NoR:   #If the user hasn't rated it yet
            # now it's time for a recommendation!
            print("give a rating")
            correlatedUserRating = ratingTable[corUser][bus] 
            
            if corValue < 0:
                #flip the correlatedUserRating since its negative
                correlatedUserRating = 1-ratingTable[corUser][bus]  
                    
            if bus not  in recArr:
                recArr[bus] = {}
                recArr[bus]['sum'] = 0
                recArr[bus]['tot'] = 0            
            recArr[bus]['tot'] = recArr[bus]['tot'] + 1
            recArr[bus]['sum'] = recArr[bus]['sum'] + correlatedUserRating
   

def pearson_correlation():
    global g_NegR
    global g_PosR
    global g_NeuR
    global g_NoR
    corArr = dict()  #a dict of dicts to keep track of correlated users
    
    ratingTable = get_rating_table_working_copy()
    #1.) Calculated the pearson correlation between users
    for user in ratingTable:    
        corArr[user] = get_listof_most_similar_users(ratingTable, user)
    
    #2.) Calculate recommendations based on the correlations
    for user in corArr:
        runRec = dict() #a dict of a 3-tuple keeping running track of the recommendations from the correlated users
        correlatedUsers = corArr[user]
        for (corUser, corValue) in correlatedUsers:
            #sufficiently positive or negative
            if sufficiently_correlated(corValue):
                print("Sufficiently Correlated")
                #calculate the recommendations for this (user, correlatedUser) pair and all businesses
                calculate_recommendation_allbusinesses(user, corUser, corValue, ratingTable, runRec)
        #now we have a running recommendation vector filled with everything we need. We simply plug it into 
        # the ci_lowerbound func
        for bus in ratingTable[user]:
            if bus in runRec:
                print("there is some")
                # no recommmendation, o well
                numPositive = runRec[bus]['pos']
                numNegative = runRec[bus]['neg']
                numTotal = runRec[bus]['tot']
                rec = -1
                if numPositive > numNegative:
                    rec = g_PosR
                else:
                    rec = g_NegR
                print("recommendation for " +user+" to bus "+bus+" is "+rec)
                insertRecommendation(user, bus, rec)
                    
                


            
            
                
    
            
            
    
            
