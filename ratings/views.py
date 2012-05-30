from django.contrib.auth import logout
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from ratings.forms import BusinessForm
from ratings.models import Business, Grouping, Rating, Keyword, Review, Tip
from ratings.populate import create_business, create_keyword
from ratings.utility import getNumRatings, log_msg
from recommendation.normalization import getBusAvg, getNumPosRatings, \
        getNumNegRatings
from recommendation.recengine import RecEngine
import json


re = RecEngine()


def top_ten(request):
    if request.user.is_authenticated():
        top10 = re.get_top_ratings(request.user, 25)
        for b in top10:
            b.average_rating = round(getBusAvg(b.id) * 2) / 2

        return render_to_response('ratings/top.html', {'user': request.user, 'business_list': top10}, context_instance=RequestContext(request))


def detail_keywords(request, bus_id):
    b = get_object_or_404(Business, pk=bus_id)
    if request.method == 'POST':
        #add a keyword
        form = request.POST
        if 'name' in form:  # we're posting a keyword
            nm = form['name']
            try:
                k = Keyword.objects.get(name=nm)
            except:
                k = create_keyword(name=nm)
            gset = Grouping.objects.filter(business=b, keyword=k)
            if gset.count() == 0:
                g = Grouping.objects.create(business=b, keyword=k)
                g.save()
        if 'review' in form:  # we're posting a review
            review = form['review']
            rev = Review.objects.create(user=request.user, business=b, descr=review)
            rev.save()
        if 'tip' in form:  # we're posting a tip
            tip = form['tip']
            tip = Tip.objects.create(user=request.user, business=b, descr=tip)
            tip.save()
    keywords = b.keywords
    tips = Tip.objects.filter(business=b)
    reviews = Review.objects.filter(business=b)
    return render_to_response('ratings/detail.html', {'business': b, 'keywords': keywords, 'tips': tips, 'reviews': reviews}, context_instance=RequestContext(request))


def get_keywords(request):
    if request.method == 'GET':
        q = request.GET.get('term', '')
        keywords = Keyword.objects.filter(name__icontains=q)[:20]
        results = []
        for word in keywords:
            results.append(word.name)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def add_keyword(request):
    log_msg('Create a keyword')
    if request.method == 'POST':  # add a keyword!
        form = request.POST

        nm = form['name']
        keyset = Keyword.objects.filter(name=nm)
        print(set)
        if(keyset.count() == 0):
            k = Keyword.objects.create(name=nm)
            print('new one')
            k.save()
    else:
        return render_to_response('ratings/add_keyword.html', {'keywords': Keyword.objects.all()}, context_instance=RequestContext(request))


def add_business(request):
    log_msg('Create a business')
    if request.method == 'POST':  # add a business
        form = BusinessForm(request.POST)
        name = form.data['name']
        address = form.data['address']
        city = form.data['city']
        state = form.data['state']

        b = create_business(name, address, state, city, 1, 1)
        b.save()
        return render_to_response('ratings/detail.html', {'business': b, 'avg': 0, 'numRatings': 0}, context_instance=RequestContext(request))
    else:  # Print a boring business form
        f = BusinessForm()
        return render_to_response('ratings/add_business.html', {'form': f}, context_instance=RequestContext(request))


def rate(request, bus_id):
    return HttpResponse("You're rating for business %s." % bus_id)


def index(request):
#               global re
#               re.spawn_worker_task()
#       if request.user.is_authenticated():
    business_list = Business.objects.all()
    for b in business_list:
        b.average_rating = round(getBusAvg(b.id) * 2) / 2

        b.num_ratings = getNumRatings(b.id)
        if request.user.is_authenticated():
            b.pos_ratings = getNumPosRatings(b)
            b.neg_ratings = getNumNegRatings(b)
            thisRat = Rating.objects.filter(username=request.user, business=b)
            if thisRat.count() > 0:
                r = Rating.objects.get(username=request.user, business=b)
                b.this_rat = r.rating
            else:
                b.this_rat = 0
    paginator = Paginator(business_list, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        business_list = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        business_list = paginator.page(1)
    except EmptyPage:
        business_list = paginator.page(paginator.num_pages)
    return render_to_response('ratings/index.html', {'business_list': business_list}, context_instance=RequestContext(request))


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')



#def pop_test_data(request):
#       log_msg('Populating with test data')
#       numUsers = 10
#       numBusinesses =20
#       populate_test_data(numUsers, numBusinesses)
#       return HttpResponseRedirect('/')
#

#def detail(request, bus_id):
#       global re
#       b = get_object_or_404(Business, pk=bus_id)
#       avg = round(getBusAvg(b.id)*2)/2
#       numRatings = getNumRatings(b)
#       if request.user.is_authenticated():
#               try:
#                       r = Rating.objects.get(username=request.user, business=bus_id)   #rating exists
#                       if request.method == 'POST':    #posting an existing rating
#                               form = RatingForm(request.POST)
#                               if form.is_valid():
#                                       cd = form.cleaned_data
#                                       new_rating = cd['rating']
#                                       r.rating        = new_rating
#                                       r.save()
#                       f2 = RatingForm();
#                       return render_to_response('ratings/detail.html', {'business': b,'rating': r, 'form' : f2, 'avg':avg, 'numRatings':numRatings}, context_instance=RequestContext(request))
#               except: #rating doesn't exist
#                       if request.method == 'POST':    # posting a new rating
#                               form = RatingForm(request.POST)
#                               if form.is_valid():
#                                       cd = form.cleaned_data
#                                       new_rating = cd['rating']
#                                       r = Rating.objects.create(business=b, username=request.user,rating=new_rating)
#                                       r.save()
#                                       f2 = RatingForm();
#                                       return render_to_response('ratings/detail.html', {'business': b,'rating': r , 'form' : f2, 'avg':avg, 'numRatings':numRatings}, context_instance=RequestContext(request))
#                       else:
#                               f2 = RatingForm();
#                               r = re.get_best_current_recommendation(b, request.user)
#                               return render_to_response('ratings/detail.html', {'business': b, 'form' : f2, 'recommendation': r, 'avg': avg, 'numRatings': numRatings}, context_instance=RequestContext(request))
#       else:           # Not logged in
#               p = get_object_or_404(Business, pk=bus_id)
#
#               return render_to_response('ratings/detail.html', {'business': p, 'avg':avg, 'numRatings':numRatings}, context_instance=RequestContext(request))
#



#def reset_site(request):
#       read_dataset()
#       build_pred_server()
#
#def display_table_full(request):
#       return display_table(request, 500)
#
#def display_table(request, maxc):
#       maxc=int(maxc)
#       business_list = Business.objects.all()
#       user_list = User.objects.all()
#       bus_to_display = []
#       all_ratings = []
#       userno = 0
#
#       c = 0
#       for b in business_list:
#               if  c > maxc:
#                       break
#               c+=1
#               bus_to_display.append(b)
#
#       for user in user_list:
#               if(userno >maxc):
#                       break
#               businessno = 0
#               all_ratings.append([user.username])
#               for business in business_list:
#                       if(businessno > maxc):
#                               break
#                       try:
#                               r = Rating.objects.get(username=user, business=business).rating
#                               all_ratings[userno].append(r)
#                       except:
#                               r="--"
#                               all_ratings[userno].append(r)
#
#                       businessno = businessno+1
#               userno = userno + 1
#
#
#       #print(all_ratings)
#       return  render_to_response('ratings/rating_table.html', {'ratings_list': all_ratings, 'business_list' :bus_to_display, 'user_list': user_list}, context_instance=RequestContext(request))
