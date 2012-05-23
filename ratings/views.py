from data_import.views import read_dataset
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core import paginator
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from ratings.forms import BusinessForm, KeywordForm, RatingForm
from ratings.models import Business, Grouping, Rating
from ratings.normalization import getBusAvg, getNumPosRatings, getNumNegRatings
from ratings.populate import populate_test_data
from ratings.recengine import RecEngine
from ratings.utility import getNumRatings
from validation.views import build_pred_server
import json


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
	
def top_ten(request):
	if request.user.is_authenticated():
		top10 = re.get_top_ratings(request.user, 25)
		for b in top10:
				b.average_rating = round(getBusAvg(b.id)*2)/2
				
		return	render_to_response('ratings/top.html', {'user': request.user, 'business_list': top10}, context_instance=RequestContext(request))		

def detail(request, bus_id):
	global re
	b = get_object_or_404(Business, pk=bus_id)
	avg = round(getBusAvg(b.id)*2)/2
	numRatings = getNumRatings(b)
	if request.user.is_authenticated():
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
			return render_to_response('ratings/detail.html', {'business': b,'rating': r, 'form' : f2, 'avg':avg, 'numRatings':numRatings}, context_instance=RequestContext(request))
		except:	#rating doesn't exist
			if request.method == 'POST':	# posting a new rating
				form = RatingForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					new_rating = cd['rating']
					r = Rating.objects.create(business=b, username=request.user,rating=new_rating)
					r.save() 
					f2 = RatingForm();			
					return render_to_response('ratings/detail.html', {'business': b,'rating': r , 'form' : f2, 'avg':avg, 'numRatings':numRatings}, context_instance=RequestContext(request))
			else:
				f2 = RatingForm();		
				r = re.get_best_current_recommendation(b, request.user)	
				return render_to_response('ratings/detail.html', {'business': b, 'form' : f2, 'recommendation': r, 'avg': avg, 'numRatings': numRatings}, context_instance=RequestContext(request))
	else:		# Not logged in
		p = get_object_or_404(Business, pk=bus_id)
		
		return render_to_response('ratings/detail.html', {'business': p, 'avg':avg, 'numRatings':numRatings}, context_instance=RequestContext(request))
		
	
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
#		global re
#		re.spawn_worker_task()
#	if request.user.is_authenticated():
		business_list = Business.objects.all()
		c = Context({
			'business_list': business_list,
		})
		for b in business_list:
			b.average_rating = round(getBusAvg(b.id)*2)/2
			
			b.num_ratings=getNumRatings(b.id)
			if request.user.is_authenticated():
				b.pos_ratings = getNumPosRatings(b.id)
				b.neg_ratings = getNumNegRatings(b.id)
				thisRat = Rating.objects.filter(username=request.user, business=b)
				if thisRat.count() > 0:
					r = Rating.objects.get(username=request.user, business=b)
					b.this_rat = r.rating
				else:
					b.this_rat = 0
		paginator = Paginator(business_list, 10) # Show 25 contacts per page	
		page = request.GET.get('page')
		try:
			business_list = paginator.page(page)
		except PageNotAnInteger:
			business_list = paginator.page(1)
		except EmptyPage:
			business_list = paginator.page(paginator.num_pages)
		return	render_to_response('ratings/index.html', {'business_list': business_list}, context_instance=RequestContext(request))
	#else:
	#	return HttpResponse("log in dawg");


def reset_site(request):
	read_dataset()
	build_pred_server()

def display_table_full(request):
	return display_table(request, 500)

def display_table(request, maxc):
	maxc=int(maxc)
	business_list = Business.objects.all()
	user_list = User.objects.all()
	bus_to_display = []
	all_ratings = []
	userno = 0
	
	c = 0
	for b in business_list:
		if  c > maxc:
			break
		c+=1
		bus_to_display.append(b)
	
	for user in user_list:
		if(userno >maxc):
			break
		businessno = 0
		all_ratings.append([user.username])
		for business in business_list:
			if(businessno > maxc):
				break
			try:
				r = Rating.objects.get(username=user, business=business).rating
				all_ratings[userno].append(r)
			except:
				r="--"
				all_ratings[userno].append(r)

			businessno = businessno+1
		userno = userno + 1

	
	#print(all_ratings)
	return	render_to_response('ratings/rating_table.html', {'ratings_list': all_ratings, 'business_list' :bus_to_display, 'user_list': user_list}, context_instance=RequestContext(request))

@csrf_exempt
def vote(request):

	if request.method == 'POST':
		print("here" + str(request.POST['id']))
		try:
			business = Business.objects.get(id=request.POST['id'])
		except Business.DoesNotExist:
			return HttpResponse("{'success': 'false'}")


		if request.POST['type'] == 'up':
			rat = 5#rating.rating + 1
			res = 'pos'
		else:
			rat = 1#rating.rating - 1
			res = 'neg'
		
		try:
			rating = Rating.objects.get(business=business, username=request.user)
		except Rating.DoesNotExist:
			print("create a new rating!")
			rating = Rating.objects.create(business=business,username=request.user,rating=rat)
		else:
			print("rating already exists :(")
			return HttpResponse("{'success': 'false'}")
		rating.save()
		response_data = dict()
		response_data['id'] = str(request.POST['id'])
		response_data['success'] = 'true'
		response_data['rating'] = res
		response_data['pos_rating'] = getNumPosRatings(business)
		response_data['neg_rating'] = getNumNegRatings(business)
		
		return HttpResponse(json.dumps(response_data), mimetype="application/json")
		#return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
	else:
		raise Http404('What are you doing here?')

#from stack overflow

@csrf_exempt
def remove_vote(request):
	if request.method == 'POST':
		try:
			business = Business.objects.get(id=request.POST['id'])
		except Business.DoesNotExist:
			return HttpResponse("{'success': 'false'}")

		try:
			rating = Rating.objects.filter(business=business, username=request.user)
		except Rating.DoesNotExist:
			pass
		else:
			print('delete it!')
			rating.delete()

		response_data = dict()
		response_data['id'] = str(request.POST['id'])
		response_data['success'] = 'true'
		response_data['pos_rating'] = getNumPosRatings(business)
		response_data['neg_rating'] = getNumNegRatings(business)

		return HttpResponse(json.dumps(response_data), mimetype="application/json")
	else:
		raise Http404('What are you doing here?')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
