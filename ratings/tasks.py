from celery.decorators import periodic_task
from datetime import timedelta
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from ratings.models import Business, DontCare, Rating, Recommendation, UserMeta
from data_import.views import average_total_rating
from data_import.views import average_total_rating
from ratings.nmf import run_nmf_mult_k
import math

g_NegR = 1 #negative
g_PosR = 2 #positive
g_NeuR = 0 #neutral
g_NoR = 0 #no rating


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

#from http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
def ci_lowerbound(numPosRev, numTotalRev):
    z = 1.96 #for confidence of 0.95
    if numTotalRev == 0:
        return 0
    p_hat = 1.0 * numPosRev / numTotalRev
    return(p_hat + z * z / (2 * numTotalRev) - z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * numTotalRev) / numTotalRev) / (1 + z * z / numTotalRev)))




def buildAverageRatings():
	all_businesses = Business.objects.all()
  insBus = []
	for bus in all_businesses:
		print(bus)
		ratingFilter = Rating.objects.filter(business=bus).aggregate(Sum('rating'), Count('rating'))
		sumRating = ratingFilter[0]
		countRating = ratingFilter[1]
		avg = ci_lowerbound(sumRating, countRating)
		insertAverage(bus,avg)
    queryset = Business.objects.filter( business=bus)
	  if queryset.count() >= 1:
	  	queryset.delete()
	  r1 = Business( business=bus, average_rating=avg)
    insBus.append(r1)
  Business.objects.bulk_create(insBus)
    
  
  usermeta = []
  for user in User.objects.all():
		ratingFilter = Rating.objects.filter(username=user).aggregate(Sum('rating'), Count('rating'))
    sumRating = ratingFilter[0]
    countRating = ratingFilter[1]
    avg = ci_lowerbound(sumRating,countRating)
    meta = UserMeta(average_rating=avg, user=user)
    usermeta.append(meta)
  UserMeta.objects.bulk_create(usermeta)
  
  average_total_rating = Rating.objects.all().aggregate(Sum('rating'),Count('rating'))
  
  transaction.commit();


		
def insertRecommendation(user, bus, rec):
	queryset = Recommendation.objects.filter(username=user, business=bus)
	if queryset.count() >= 1:
		queryset.delete()
	r1 = Recommendation(username=user, business=bus, recommendation=rec)
	r1.save()



@periodic_task(name="tasks.build_recommendations", run_every=timedelta(seconds=10))
def build_recommendations():
	#working_copy = get_rating_table_working_copy()
	K = [1,5,10,15,20]
	run_nmf_mult_k()
	buildAverageRatings()
	
