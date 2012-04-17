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
from ratings.models import DontCare
from ratings.models import Recommendation
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Sum


import ratings.recengine

corPositiveBound = 0.5
corNegativeBound = -0.5

g_NegR = 0 #negative
g_PosR = 1 #positive
g_NeuR = -1 #neutral
g_NoR = -2 #no rating


#BUG!
#The ratingTable uses 0 for a no-rating, so that when I pass it to the Pearson
#function, there's no conflict in sizes of arrays

#We need ot figure out what rating values we're going to be using and then use them in all place
# We should also specify whether or not its going to be like,meh,dislike  and if meh counts as no rating at all



def get_rating_table_working_copy():
	global g_NegR
	global g_PosR
	global g_NeuR
	global g_NoR
	ratingTable = dict()
	allBusinesses = Business.objects.all()
	allUsers = User.objects.all()
	
	for u in allUsers:
		ratingTable[u] = {}
		for b in allBusinesses:
			r = Rating.objects.filter(username=u, business=b)
			if r:
				r = Rating.objects.get(username=u, business=b)
				dc = DontCare.objects.filter(username=u, business=b)
				if dc:
					ratingTable[u][b] = g_NeuR
				else:
					ratingTable[u][b] = r.rating
			else:
				ratingTable[u][b] = g_NoR
	return ratingTable



def get_listof_most_similar_users(ratingTable, thisUser):
	#an array of correlations indexed by "other users
	correlationArray = {}
	
	#iterate through all other users
	for otherUser, ratingArr in ratingTable.iteritems():	 
		thisUserOverlapRatings = []
		otherUserOverlapRatings = []
		if otherUser != thisUser:			#except for the current user
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

#from http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
def ci_lowerbound(numPosRev, numTotalRev):
	z = 1.96 #for confidence of 0.95
	if numTotalRev == 0:
		return 0
	p_hat = 1.0 * numPosRev / numTotalRev
	return(p_hat + z * z / (2 * numTotalRev) - z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * numTotalRev) / numTotalRev) / (1 + z * z / numTotalRev)))


#Given a corValue, is it big or small enough to matter
def sufficiently_correlated(corValue):
	global corNegativeBound
	global corPositiveBound
	if corValue >= corPositiveBound or corValue <= corNegativeBound:
		return True
	return False
	
	
def insertAverage(bus, avg):
	queryset = Business.objects.filter( business=bus)
	if queryset.count() >= 1:
		queryset.delete()
	#r1 = Business( business=bus, average_rating=avg)
	#r1.save()	
		
def insertRecommendation(user, bus, rec):
	queryset = Recommendation.objects.filter(username=user, business=bus)
	if queryset.count() >= 1:
		queryset.delete()
	r1 = Recommendation(username=user, business=bus, recommendation=rec)
	r1.save()


		
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


@periodic_task(name="tasks.build_recommendations", run_every=timedelta(seconds=10))
def build_recommendations():
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
					
				

	#3.)  #calculate average ratings for businesses
	#Book.objects.all().aggregate(Avg('price'))
	all_businesses = Business.objects.all()
	for bus in all_businesses:
		print(bus)
		ratingFilter = Rating.objects.filter(business=bus).aggregate(Sum('rating'), Count('rating'))
		sumRating = ratingFilter[0]
		countRating = ratingFilter[1]
		avg = ci_lowerbound(sumRating, countRating)
		insertAverage(bus,avg)
			
			
				
	
			
			
	
			
