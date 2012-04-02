from array import array
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import F
from django.http import HttpResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render_to_response, \
	render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import DetailView, ListView
from operator import itemgetter
from ratings.forms import BusinessForm, KeywordForm, RatingForm
from ratings.models import Business, Grouping, Rating

from scipy.stats.stats import pearsonr
import logging
import math
import random
import scipy



#for async queueing

from ratings.tasks import add
from celery.execute import send_task


def foo(request):
	print "zouf";
	result = send_task("tasks.add", [2, 2])
	print result.get()
	print "zouf2"

@csrf_exempt
def ajax_query(request):
	results = {'success':True}
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')


def get_rating_table():
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
	
	diffBetween = dict()
	correlationArray = {}
	for key, ratarr in ratingTable.iteritems(): 	# iterate through all ratings in teh array
		if key != user:							#except for the users
			diff = 0
			for bus  in ratarr:			# now go through all their ratings
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
	print "\n\n\n\n\n"
	print correlationArraySorted
	
	return correlationArraySorted


#Right now this is incredibly naive and stupid since it just returns the
# rating of the most similar user. This won't work for anything even reasonably complicated
def get_recommendation(business, user):
	ratingTable = get_rating_table()
	print ratingTable
	if not user in  ratingTable: 	# only works if the user has made some kind of rating
		return -1;
	else:				
		mostSimilarUsers = get_listof_most_similar_users(ratingTable, user)
		if mostSimilarUsers:
			for simUser,rating in mostSimilarUsers:
				if business in ratingTable[simUser]:
					return ratingTable[simUser][business]
	return -2
	
	
def detail(request, bus_id):
	if request.user.is_authenticated():
		b = get_object_or_404(Business, pk=bus_id)
		try: 
			r = Rating.objects.get(username=request.user, business=bus_id)	 #rating exists
			if request.method == 'POST':  #posting an existing rating
				form = RatingForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					new_rating = cd['rating']
					r.rating  = new_rating
					r.save() 
			f2 = RatingForm();
			return render_to_response('ratings/detail.html', {'business': b,'rating': r, 'form' : f2}, context_instance=RequestContext(request))
		except:	#rating doesnt exist
			if request.method == 'POST':  # posting a new rating
				form = RatingForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					new_rating = cd['rating']
					r = Rating.objects.create(business=b, username=request.user,rating=new_rating)
					r.save() 
					f2 = RatingForm();			
					return render_to_response('ratings/detail.html', {'business': b,'rating': r , 'form' : f2}, context_instance=RequestContext(request))
			else:
				f2 = RatingForm();		
				r = get_recommendation(b, request.user)	
				return render_to_response('ratings/detail.html', {'business': b, 'form' : f2, 'recommendation': r}, context_instance=RequestContext(request))
	else:    # Not logged in
		p = get_object_or_404(Business, pk=bus_id)
		return render_to_response('ratings/detail.html', {'business': p}, context_instance=RequestContext(request))
		
	
def add_keyword(request):
	if request.method == 'POST':  #add a business
		form = KeywordForm(request.POST)
		new_key = form.save()
		return HttpResponseRedirect('/')
	else: #add a form
		f = KeywordForm();			
		return render_to_response('ratings/add_keyword.html', {'form' : f}, context_instance=RequestContext(request))	




def add_business(request):
	if request.method == 'POST':  #add a business
		form = BusinessForm(request.POST)
		new_business = form.save(commit=False)
		new_business.save()
		for key_id in request.POST.getlist('keywords'):
			grouping = Grouping.objects.create(keyword_id = int(key_id), business = new_business)
		return HttpResponseRedirect('/')

	else: #add a form
		f = BusinessForm();			
		return render_to_response('ratings/add_business.html', {'form' : f}, context_instance=RequestContext(request))	


def rate(request, bus_id):
    return HttpResponse("You're rating for business %s." % bus_id)

def index(request):
		foo(request)
#	if request.user.is_authenticated():
		business_list = Business.objects.all()
		c = Context({
		  'business_list': business_list,
		})
		return  render_to_response('ratings/index.html', {'business_list': business_list}, context_instance=RequestContext(request))
	#else:
	#	return HttpResponse("log in dawg");
   



def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
