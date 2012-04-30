from array import array
from celery.execute import send_task
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
from ratings.recengine import RecEngine
from ratings.populate import populate_test_data
import sys



re = RecEngine() 

@csrf_exempt
def ajax_query(request):
	results = {'success':True}
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')


def pop_test_data(request):
	print('Populating with test data')
	numUsers = 10
	numBusinesses =20
	populate_test_data(numUsers, numBusinesses)
	return HttpResponseRedirect('/')
	

	
def detail(request, bus_id):
	global re
	if request.user.is_authenticated():
		b = get_object_or_404(Business, pk=bus_id)
		try: 
			r = Rating.objects.get(username=request.user, business=bus_id)	 #rating exists
			if request.method == 'POST':	#posting an existing rating
				form = RatingForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					new_rating = cd['rating']
					r.rating	= new_rating
					r.save() 
			f2 = RatingForm();
			return render_to_response('ratings/detail.html', {'business': b,'rating': r, 'form' : f2}, context_instance=RequestContext(request))
		except:	#rating doesnt exist
			if request.method == 'POST':	# posting a new rating
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
				r = re.get_best_current_recommendation(b, request.user)	
				return render_to_response('ratings/detail.html', {'business': b, 'form' : f2, 'recommendation': r}, context_instance=RequestContext(request))
	else:		# Not logged in
		p = get_object_or_404(Business, pk=bus_id)
		return render_to_response('ratings/detail.html', {'business': p}, context_instance=RequestContext(request))
		
	
def add_keyword(request):
	if request.method == 'POST':	#add a business
		form = KeywordForm(request.POST)
		new_key = form.save()
		return HttpResponseRedirect('/')
	else: #add a form
		f = KeywordForm();			
		return render_to_response('ratings/add_keyword.html', {'form' : f}, context_instance=RequestContext(request))	




def add_business(request):
	if request.method == 'POST':	#add a business
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
		global re
		re.spawn_worker_task()
#	if request.user.is_authenticated():
		business_list = Business.objects.all()
		c = Context({
			'business_list': business_list,
		})
		return	render_to_response('ratings/index.html', {'business_list': business_list}, context_instance=RequestContext(request))
	#else:
	#	return HttpResponse("log in dawg");

def display_table_full(request):
	return display_table(request, 500)

def display_table(request, maxc):
	maxc=int(maxc)
	business_list = Business.objects.all()
	user_list = User.objects.all()
	all_ratings = []
	userno = 0
	for user in user_list:
		businessno = 0
		all_ratings.append([user.username])
		for business in business_list:
			try:
				r = Rating.objects.get(username=user, business=business).rating
				all_ratings[userno].append(r)
			except:
				r="--"
				all_ratings[userno].append(r)
			businessno = businessno+1
			if(businessno > maxc):
				break
		userno = userno + 1
		if(userno >maxc):
			break
	
	#print(all_ratings)
	return	render_to_response('ratings/rating_table.html', {'ratings_list': all_ratings, 'business_list' :business_list, 'user_list': user_list}, context_instance=RequestContext(request))




def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
