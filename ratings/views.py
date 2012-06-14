from comments.views import get_comments
from django.contrib.auth import logout
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from photos.models import BusinessPhoto
from photos.views import get_photo_thumb_url
from ratings.forms import BusinessForm
from ratings.models import Business
from ratings.populate import create_business
from ratings.search import search_site
from ratings.utility import get_lat, get_bus_data
from recommendation.normalization import getBusAvg
from recommendation.recengine import RecEngine
from tags.views import get_tags
import logging


logger = logging.getLogger(__name__)

re = RecEngine()

def coming_soon(request):
    if request.user.is_authenticated():
        return index(request)
    else:
        return render_to_response('coming_soon.html', context_instance=RequestContext(request))



def top_ten(request):
    if request.user.is_authenticated():
        top10 = re.get_top_ratings(request.user, 25)
        for b in top10:
            b.average_rating = round(getBusAvg(b.id) * 2) / 2

        return render_to_response('ratings/top.html', {'user': request.user, 'business_list': top10}, context_instance=RequestContext(request))



def search_test(request):
    form = request.GET
    if 'search' not in form:
        return index(request)
    term = form['search']
    business_list = search_site(term)
    businesses = get_bus_data(business_list,request.user)
    paginator = Paginator(businesses, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        businesses = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        businesses = paginator.page(1)
    except EmptyPage:
        businesses = paginator.page(paginator.num_pages)
    return render_to_response('ratings/index.html', {'business_list': businesses, 'search_term': term}, context_instance=RequestContext(request))

    

@csrf_exempt
def detail_keywords(request, bus_id):
    b = get_object_or_404(Business, pk=bus_id)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
#        form = request.POST

#        if 'tip' in form:  # we're posting a tip
#            tip = form['tip']
#            tip = Tip.objects.create(user=request.user, business=b, descr=tip)
#            tip.save()
#        if 'tag' in form:
#            tag = form['tag']
#            tag = Tag.objects.create(creator=request.user, business=b, descr=tag)
#            tag.save()

    
    comments = get_comments(b,user=request.user,q="")
    tags = get_tags(b,user=request.user,q="")
        
    latlng = get_lat(b.address + " " + b.city + ", " + b.state)
    try:
        b.photourl = get_photo_thumb_url(b)
    except:
        b.photourl= "" #NONE

    if latlng:
        return render_to_response('ratings/detail.html', {'business': b, 'tags': tags, 'comments': comments, 'lat':latlng[0], 'lng':latlng[1]}, context_instance=RequestContext(request))
    else:
        return render_to_response('ratings/detail.html', {'business': b, 'tags': tags, 'comments': comments}, context_instance=RequestContext(request))


def add_business(request):
 
    if request.method == 'POST':  # add a business
        form = BusinessForm(request.POST, request.FILES)
        name = form.data['name']
        logger.debug("Creation of business %s by  %s", name,request.user.username)
        address = form.data['address']
        city = form.data['city']
        state = form.data['state']
        img = request.FILES['image']

        b = create_business(name, address, state, city, 1, 1)
        b.save()
       
        bp = BusinessPhoto(user=request.user, business=b, image=img, title="test main", caption="test cap")
        bp.save()
        return detail_keywords(request,b.id)
    else:  # Print a boring business form
        f = BusinessForm()
        return render_to_response('ratings/add_business.html', {'form': f}, context_instance=RequestContext(request))




def index(request):
    business_list = get_bus_data(Business.objects.all(),request.user)
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


