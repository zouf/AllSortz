from communities.models import UserMembership, Community, BusinessMembership
from communities.views import get_community, get_default
from django.contrib.auth import logout
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from photos.models import BusinessPhoto
from photos.views import get_photo_thumb_url, get_photo_web_url
from ratings.forms import BusinessForm, CommentForm
from ratings.models import Business, Comment, CommentRating
from ratings.populate import create_business
from ratings.search import search_site
from ratings.utility import get_lat, get_bus_data
from recommendation.normalization import getBusAvg, getNumPosRatings, \
    getNumNegRatings
from recommendation.recengine import RecEngine
from tags.models import CommentTag, Tag
from tags.views import get_tags, get_pages, get_tags_user
from wiki.forms import PageForm
from wiki.models import Page
from wiki.views import view
import logging
import sys


logger = logging.getLogger(__name__)

re = RecEngine()
def comment_comp(x,y):
    #eventually do something more intelligent here!
    xTot = x.pos_ratings - x.neg_ratings
    yTot = y.pos_ratings - y.neg_ratings
    if (xTot > yTot):
        return -1
    elif (xTot < yTot ):
        return 1
    else:
        return 0




#gets all the comments, including nested ones
#adds tokens "open" and "close" to denote subcomments
def get_comments(b,user=False,q=""):
    if q != "":
        comments = Comment.objects.filter(descr__icontains=q)[:20]
    else:
        comments = Comment.objects.filter(business=b)
    
  
    comment_list = []
    for c in comments:
        if c.reply_to is None:
            comment_list.append("open")
            recurse_comments(c,comment_list)
            comment_list.append("close")
    
    results = []              
    for c in comment_list:
        if c != "open" and c != "close":
            try:
                rat =  CommentRating.objects.get(comment=c)
                c.this_rat = rat.rating
                c.pos_ratings = getNumPosRatings(c)
                c.neg_ratings = getNumNegRatings(c)
            except:
                c.this_rat = 0
                c.pos_ratings = 0
                c.neg_ratings = 0
        results.append(c)
    return results



def add_comment_form(request,bus_id):
    business = get_object_or_404(Business, pk=bus_id)
    if request.method == 'POST':  # add a business
        form = CommentForm(request.POST)
        descr = form.data['descr']
        tags = request.POST.getlist('tag')

        c = Comment(user = request.user, business=business,descr=descr)
        c.save()
        
        for t in tags:
            try:
                ct = CommentTag(descr=t , comment=c,creator=request.user)
                try:
                    tags = Tag.objects.get(descr=t)
                except:
                    tag = Tag(descr=t,creator=request.user,business=business)
                    tag.save()
                ct.save()
            except:
                print('error in creating a tag for comments')
                logger.error("somethign went wrong in creating a tag for comments")
        
        
        return redirect(detail_keywords,bus_id)
        #return detail_keywords(request,bus_id)
        
    else:  # Print a boring business form
        f = CommentForm()
        return render_to_response('comments/add_comment.html', {'form': f}, context_instance=RequestContext(request))




#adds comments to the database
@csrf_exempt
def add_comment(request):
    logger.debug('in add comment')
    if request.method == 'POST':  # add a comment!
        form = request.POST       
        #base comment submission
        if 'cid' not in form:      
            nm = form['comment']
            bid = form['bid']
            b = Business.objects.get(id=bid)
            keyset = Comment.objects.filter(descr=nm, business=b)
            if(keyset.count() == 0):
                try:
                    k = Comment.objects.create(descr=nm,user=request.user,business=b,reply_to=None)
                except:
                    logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                k.save()
        else:  #reply to another comment submission
            nm = form['comment']
            bid = form['bid']
            b = Business.objects.get(id=bid)
            cid = form['cid']
            c = Comment.objects.get(id=cid)
            keyset = Comment.objects.filter(descr=nm, business=b)
            if(keyset.count() == 0):
                try:
                    k = Comment.objects.create(descr=nm,user=request.user,business=b,reply_to=c)
                except:
                    logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                k.save()
        comment_list = get_comments(b)
        return render_to_response('comments/thread.html', {'business':b, 'comments': comment_list})



def recurse_comments(comment,cur_list):
    cur_list.append(comment)
    replies = Comment.objects.filter(reply_to=comment)
    for c in replies:
        cur_list.append("open")
        recurse_comments(c,cur_list)
        cur_list.append("close")



def coming_soon(request):
    if request.user.is_authenticated():
        return index(request)
    else:
        return render_to_response('coming_soon.html', context_instance=RequestContext(request))





def search(request):
    form = request.GET
    if 'search' not in form:
        return index(request)
    term = form['search']
    location = form['location']
    
    #TODO fix getting location
    if location == "":
        #handle blank location with IP track!!!
        location = get_default()
        
    business_list = search_site(term, location)
    businesses = get_bus_data(business_list,request.user)
    paginator = Paginator(businesses, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        businesses = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        businesses = paginator.page(1)
    except EmptyPage:
        businesses = paginator.page(paginator.num_pages)
    return render_to_response('ratings/onetag.html', {'business_list': businesses, 'search_term': term, 'location_term':location}, context_instance=RequestContext(request))


def edit_tag_discussion(request,bus_id,page_id):
    b = get_object_or_404(Business, pk=bus_id)
    page = get_object_or_404(Page, pk=page_id)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if not page:
                page = Page()
            page.content = form.cleaned_data['content']

            page.save()
            return redirect(detail_keywords, bus_id=bus_id)
    else:
        if page:
            wiki_edit_form = PageForm(initial=page.__dict__)
        else:
            wiki_edit_form = PageForm(initial={'name': page.name})


        
    comments = get_comments(b,user=request.user,q="")
        
    latlng = get_lat(b.address + " " + b.city + ", " + b.state)
    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE

    if latlng:
        context =   { \
        'business' : b, \
        'comments': comments, \
        'lat': latlng[0],\
        'lng':latlng[1],  \
         'form': wiki_edit_form,\
        'page': page \
        }
    else:
        context = \
        { \
        'business' : b, \
        'comments': comments, \
         'form': wiki_edit_form, \
         'page': page \
        }
    return render_to_response('ratings/detail.html',
        RequestContext(request, context))


@csrf_exempt
def detail_keywords(request, bus_id):
    b = get_object_or_404(Business, pk=bus_id)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    comments = get_comments(b,user=request.user,q="")
    tags = get_tags(b,user=request.user,q="")
        
    pages = get_pages(b,tags)
    latlng = get_lat(b.address + " " + b.city + ", " + b.state)
    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE

    if latlng:
        context =   { \
        'business' : b, \
        'comments': comments, \
        'lat': latlng[0],\
        'lng':latlng[1],  \
        'tags':tags, \
        'pages': pages \
        }
    else:
        context = \
        { \
        'business' : b, \
        'comments': comments, \
        'tags':tags, \
        'pages': pages \
        }
    
    return render_to_response('ratings/detail.html', context_instance=RequestContext(request,context))


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
        
        community = get_community(request.user)
        
        bm = BusinessMembership(business=b,community=community)
        bm.save()
        
        return redirect(detail_keywords,b.id)
    else:  # Print a boring business form
        f = BusinessForm()
        return render_to_response('ratings/add_business.html', {'form': f}, context_instance=RequestContext(request))



def paginate_businesses(business_list,page, num):
    paginator = Paginator(business_list, num)  # Show 25 contacts per page
    try:
        business_list = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        business_list = paginator.page(1)
    except EmptyPage:
        business_list = paginator.page(paginator.num_pages)
    return business_list

def index(request):
    
    community = get_community(request.user)
    businesses = []
    try:
        busMembership = BusinessMembership.objects.filter(community = community)
        for b in busMembership:
            businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    
    business_list = get_bus_data(businesses,request.user)
    business_list = paginate_businesses(business_list,request.GET.get('page'),1)

    return render_to_response('ratings/index.html', {'business_list': business_list, 'community':community}, context_instance=RequestContext(request))

def user_details(request):
    if not request.user.is_authenticated():
        return redirect(index)
    
    tags = get_tags_user(request.user,"")
    
    context = {\
        'user': request.user,\
        'tags':tags\
    }
    
    return render_to_response('ratings/user/user_detail.html', context_instance=RequestContext(request,context))
    


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


