from communities.forms import CommunityForm
from communities.models import BusinessMembership, UserMembership
from communities.views import get_community, get_default
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from endless_pagination.decorators import page_template
from photos.models import BusinessPhoto
from photos.views import get_photo_web_url
from ratings.contexts import get_tag_comments, get_business_comments, \
    get_default_blank_context, get_default_tag_context, get_default_bus_context, \
    get_unauthenticated_context
from ratings.favorite import get_user_favorites, is_user_subscribed
from ratings.forms import BusinessForm, CommentForm
from ratings.models import Business, Comment, CommentRating, TagComment, \
    PageRelationship, BusinessComment, Community, Rating
from ratings.populate import create_business
from ratings.search import search_site
from ratings.utility import get_lat, get_bus_data, get_single_bus_data, \
    get_businesses_by_tag, get_businesses_by_community, get_businesses_trending, \
    get_businesses_by_your
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from recommendation.recengine import RecEngine
from tags.form import HardTagForm, TagForm
from tags.models import CommentTag, Tag, BusinessTag, UserTag, HardTag, \
    BooleanQuestion
from tags.views import get_questions, get_master_summary_tag, add_tag_to_bus
from usertraits.models import TraitRelationship, Trait
from usertraits.views import get_user_traits
from wiki.forms import PageForm
from wiki.models import Page
import datetime
import logging
import sys
import time





logger = logging.getLogger(__name__)

re = RecEngine()



@csrf_exempt
def add_tag_comment(request):
    logger.debug('in add comment')
    if request.method == 'POST':  # add a comment!
        form = request.POST 
        #add a comment to a business' tag page 
        if 'tid'  in form:
            bid =form['bid']
            b = Business.objects.get(id=bid)
            tid = form['tid']
            t = Tag.objects.get(id=tid)
            if 'cid' not in form:  #root reply
                nm = form['comment']
                k = Comment(descr=nm,user=request.user,reply_to=None)
                k.save()
                tc = TagComment(business=b,tag=t,thread=k)
                tc.save()
            else:  #reply to another comment submission
                nm = form['comment']
                cid = form['cid']
                parent = Comment.objects.get(id=cid) #parent comment
                k = Comment.objects.create(descr=nm,user=request.user,reply_to=parent) #new child
                k.save()
            comment_list = get_tag_comments(b,t)
            return render_to_response('ratings/discussion/thread.html', {'tag':t, 'business': b, 'comments': comment_list})
        
        # add a comment to a business's page alone
        else:
            bid =form['bid']
            b = Business.objects.get(id=bid)
            if 'cid' not in form:      #root reply
                nm = form['comment']
                k = Comment(descr=nm,user=request.user,reply_to=None)
                k.save()
                bc = BusinessComment(business=b,thread=k)
                bc.save()
            else:  #reply to another comment submission
                nm = form['comment']
                cid = form['cid']
                parent = Comment.objects.get(id=cid) #parent comment
                k = Comment.objects.create(descr=nm,user=request.user,reply_to=parent)
                k.save()
            comment_list = get_business_comments(b)
            return render_to_response('ratings/discussion/thread.html', {'business':b, 'comments': comment_list})






def coming_soon(request):
    if request.user.is_authenticated():
        return index(request)
    else:
        return render_to_response('coming_soon.html', context_instance=RequestContext(request))




@page_template("ratings/listing/entry.html") # just add this decorator
def display_tag(request,tag_id,extra_context=None):
    t = get_object_or_404(Tag, pk=tag_id)
    businesses = get_businesses_by_tag(t,request.user, request.GET.get('page'))
    
    try:
        UserTag.objects.get(tag=t,user=request.user)
        subscribed=True
    except:
        subscribed=False

    context = get_default_blank_context(request.user)
    context['search_term'] = t.descr
    context['all_businesses'] = businesses
    context['subscribed'] = subscribed
    context['page_template'] = "ratings/listing/entry.html"
    return render_to_response('ratings/sort.html',  context_instance=RequestContext(request,context))

    

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
    businesses = get_bus_data(business_list,request.user,True)
        

    context = get_default_blank_context(request.user)
    context['search_term'] = term
    context['business_list'] = businesses
    context['nonempty'] = True
    context.update( {
        'all_businesses' : businesses,
        'page_template': "ratings/listing/entry.html",
    } )
    return render_to_response('ratings/sort.html',  context_instance=RequestContext(request,context))




def edit_master_tag_discussion(request,bus_id,page_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
        
    b = get_object_or_404(Business, pk=bus_id)
    page = get_object_or_404(Page, pk=page_id)

    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE
    



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

    
    try:
        pgr = PageRelationship.objects.get(page=page)
    except:
        pgr = PageRelationship.objects.filter(page=page)[0]
    t = pgr.tag
    context = get_default_bus_context(b, request.user)
    context['form']=wiki_edit_form
    context['page']=page
    context['tag'] =t 
    

    
    return render_to_response('ratings/busdetail.html', context_instance=RequestContext(request,context))




def edit_tag_discussion(request,bus_id,page_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
        
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

    
    try:
        pgr = PageRelationship.objects.get(page=page)
    except:
        pgr = PageRelationship.objects.filter(page=page)[0]
    t = pgr.tag
    context = get_default_tag_context(b, t, request.user)
    context['form']=wiki_edit_form
    context['page']=page
    context['tag'] =t 
    
    for tc in context['comments']:
        print(tc)
    
    
    return render_to_response('ratings/busdetail.html',
        RequestContext(request, context))



@csrf_exempt
def detail_keywords(request, bus_id):
    b = get_object_or_404(Business, pk=bus_id)

    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE
    
    context = get_default_bus_context(b, request.user)
    context['following_business'] = is_user_subscribed(b,request.user)
    
    
    return render_to_response('ratings/busdetail.html', context_instance=RequestContext(request,context))


def add_new_tag(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    #adding a new sort
    if request.method=='POST':
        form = TagForm(request.POST,request.FILES)
        descr = form.data['descr']    
        Tag.objects.create(creator=request.user,descr=descr)

    context = get_default_blank_context(request.user)
    context['form'] =  TagForm()         
    context['type'] = 'tag'   
    return render_to_response('ratings/contribute/add_content.html',context, context_instance=RequestContext(request))


def add_community(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
        
    #post a question 
    if request.method=='POST':
        form = CommunityForm(request.POST,request.FILES)
        descr = form.data['descr']
        city = form.data['city']
        state = form.data['state']
        name = form.data['name']
        Community.objects.create(name=name,descr=descr,state=state,city=city)

    context = get_default_blank_context(request.user)
    context['form'] =CommunityForm     
    context['type'] = 'community'
    return render_to_response('ratings/contribute/add_content.html',context, context_instance=RequestContext(request))


def add_question(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
        
    #post a question 
    if request.method=='POST':

        form = HardTagForm(request.POST)
        question = form.data['question'] 
        if 'tag' in form.data:
            descr = form.data['tag']
        else:
            descr = 'unset'
        HardTag.objects.create(creator=request.user,question=question,descr=descr)

    f = HardTagForm()
    context = get_default_blank_context(request.user)
    context['form'] = f
    context['type'] = 'question'
    return render_to_response('ratings/contribute/add_content.html', context, context_instance=RequestContext(request))

def ans_business_questions(request,bus_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    if request.method != 'POST':
        b = get_object_or_404(Business, pk=bus_id)
        try:
            b.photourl = get_photo_web_url(b)
        except:
            b.photourl= "" #NONE
        questions = get_questions(b,request.user)
        b = get_single_bus_data(b,request.user)

        context = get_default_bus_context(b, request.user)
        context['questions'] = questions
        return render_to_response('ratings/contribute/ans_questions.html', context_instance=RequestContext(request,context))
    else:
        
        bid = request.POST['bid']
        values = []
        #get the list of anwers
        print(request.POST)
        for key in request.POST:
            if key.find('answer') > -1:
                values.append(request.POST[key])
                
        b = Business.objects.get(id=bid)
        
        for v in values:
            ans = v.split('_')[1]
            qid = v.split('_')[0]
            hardtag = HardTag.objects.get(id=qid)
            if ans == 'y':
                BooleanQuestion.objects.create(hardtag=hardtag,business = b,user=request.user,agree=True)
            else:
                BooleanQuestion.objects.create(hardtag=hardtag,business = b,user=request.user,agree=False) 
        return redirect(detail_keywords,bus_id)

def add_business(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
        
    if request.method == 'POST':  # add a business

        form = BusinessForm(request.POST, request.FILES)
        name = form.data['name']
        logger.debug("Creation of business %s by  %s", name,request.user.username)
        address = form.data['address']
        city = form.data['city']
        state = form.data['state']
        
        loc = address + " " + city + " " + state
        latlng = get_lat(loc)
        
        if latlng:
            b   = create_business(name, address, state, city, lat=latlng[0], lon =latlng[1])
        else:
            b = create_business(name, address, state, city, lat=0, lon =0)
            
   
  
        if 'image' in request.FILES:
            img = request.FILES['image']
            print(img)
            bp = BusinessPhoto(user=request.user, business=b, image=img, title="test main", caption="test cap")
            bp.save(True)
   
        community = get_community(request.user)
        
        bm = BusinessMembership(business=b,community=community)
        bm.save()
        
        values = request.POST.getlist('answers')
        for v in values:
            ans = v.split('_')[1]
            qid = v.split('_')[0]
            hardtag = HardTag.objects.get(id=qid)
            if ans == 'y':
                BooleanQuestion.objects.create(hardtag=hardtag,business = b,user=request.user,agree=True)
            else:
                BooleanQuestion.objects.create(hardtag=hardtag,business = b,user=request.user,agree=False) 
        
        return redirect(detail_keywords,b.id)
    else:  # Print a  business form
        context = get_default_blank_context(request.user)
        context['questions'] = get_questions(None,request.user)
        context['form'] = BusinessForm()
        return render_to_response('ratings/contribute/add_business.html', context, context_instance=RequestContext(request))

#@page_template("ratings/listing/entry.html") # just add this decorator
#def entry_list(request,template='ratings/listing/entry_list.html',extra_context=None):
#    context = {'all_businesses' : get_businesses_trending(request.user,request.GET.get('page'),[],True),
#               'your_businesses' :get_businesses_by_your(request.user,request.GET.get('page'),[],True), 
#               'community_businesses' :get_businesses_by_community(request.user,request.GET.get('page'),[],True)
#            }
#
#               
#               
#    if extra_context is not None:
#        context.update(extra_context)
#    return render_to_response(template, context,
#        context_instance=RequestContext(request))

@page_template("ratings/listing/entry.html") # just add this decorator
def index(request, template='ratings/index.html',
    extra_context=None):

    if request.user.is_authenticated():
        current_businesses = []
        
        community_businesses = get_businesses_by_community(request.user,request.GET.get('page'),[],True)
        current_businesses+=community_businesses#.object_list
        

        all_businesses = get_businesses_trending(request.user,request.GET.get('page'),[],True)
        current_businesses+=all_businesses#.object_list


        your_businesses = get_businesses_by_your(request.user,request.GET.get('page'),[],True)
        current_businesses+=your_businesses#.object_list

        context = get_default_blank_context(request.user)
        context['community_businesses'] = community_businesses
        context['your_businesses'] = your_businesses
        context['all_businesses'] = all_businesses

        context['feed'] = get_recent_activity()

        context['nonempty'] = True
        context.update( {
            'all_businesses' : all_businesses,
            'your_businesses' : your_businesses,
            'community_businesses' : community_businesses,

            'page_template': "ratings/listing/entry.html",
        } )
        return render_to_response(template, context_instance=RequestContext(request,context))
    else:
        businesses = []
        try:
            busMembership = BusinessMembership.objects.filter(community = get_default())
            for b in busMembership:
                businesses.append(b.business)
        except:
            logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
            businesses = Business.objects.all()
               
        context = get_unauthenticated_context()
        return render_to_response('ratings/index.html', context_instance=RequestContext(request,context))



def get_recent_activity():
 
    ratings = Rating.objects.filter().order_by('-date')[:5]
   
    feed = []
    
    for r in ratings:
        r.type = "business"
        r.business = get_single_bus_data(r.business, r.user, isSideBar=True)
        feed.append(r)
    allcomments = Comment.objects.filter().order_by('-date')
    for c in allcomments:
        try: 
            tc = TagComment.objects.get(thread=c)
            tc.type = "tagcomment"
            tc.business = get_single_bus_data(tc.business, c.user, isSideBar=True)
            tc.user = c.user
            feed.append(tc)
        except:
            pass
        
        try:
            bc = BusinessComment.objects.get(thread=c)
            bc.business = get_single_bus_data(bc.business, c.user, isSideBar=True)
            bc.type = "buscomment"
            bc.user = c.user
            feed.append(bc)
        except:
            pass
    return feed
    
    
    

def get_user_activity(user):
 
    ratings = Rating.objects.filter(user=user).order_by('-date')[:5]
   
    feed = []
    
    for r in ratings:
        r.type = "business"
        r.business = get_single_bus_data(r.business, user, isSideBar=True)
        feed.append(r)
    allcomments = Comment.objects.filter(user=user).order_by('-date')
    for c in allcomments:
        try: 
            tc = TagComment.objects.get(thread=c)
            tc.type = "tagcomment"
            tc.business = get_single_bus_data(tc.business, user, isSideBar=True)
            feed.append(tc)
        except:
            pass
        
        try:
            bc = BusinessComment.objects.get(thread=c)
            bc.business = get_single_bus_data(bc.business, user, isSideBar=True)
            bc.type = "buscomment"
            feed.append(bc)
        except:
            pass
    return feed
    
    
    
    

def user_details(request,uid):
    if not request.user.is_authenticated():
        return redirect(index)
  
    context = get_default_blank_context(request.user)
    communities = []
    for um in UserMembership.objects.filter(user=request.user):
        communities.append(um.community)
    context['user_communities'] = communities
    context['user_favorites'] = get_user_favorites(request.user)
    context['user_traits'] = get_user_traits(request.user)
    
    checkon = User.objects.get(id=uid)

    context['checkon'] = checkon
    context['feed'] = get_user_activity(checkon)
    return render_to_response('ratings/user/user_detail.html', context_instance=RequestContext(request,context))
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


