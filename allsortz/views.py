# Create your views here.
'''
Created on Jun 27, 2012

@author: zouf
'''
from allsortz.feed import get_all_recent_activity, get_bus_recent_activity, \
    get_user_recent_activity
from allsortz.search import search_site
from comments.models import Comment, TagComment, BusinessComment, PhotoComment
from communities.models import BusinessMembership, Community, UserMembership
from communities.views import get_default, get_community
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from endless_pagination.decorators import page_template
from photos.views import get_photo_web_url, get_all_bus_photos, \
    get_user_profile_pic
from ratings.favorite import is_user_subscribed, get_user_favorites
from ratings.models import CommentRating, Business, PageRelationship
from ratings.utility import get_bus_data, get_businesses_by_community, \
    get_businesses_trending, get_businesses_by_your, get_businesses_by_tag, \
    get_single_bus_data
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, UserTag, HardTag
from tags.views import get_tags_user, get_top_tags, get_all_sorts, \
    get_tags_business, get_hard_tags, get_pages, get_master_summary_tag
from usertraits.form import TraitForm
from usertraits.models import Trait
from usertraits.views import get_user_traits
from wiki.forms import PageForm
from wiki.models import Page
import logging





logger = logging.getLogger(__name__)

################################# Context generation #########################################


def get_default_tag_context(b,t,user):
    context = get_default_bus_context(b, user)
    comments = get_tag_comments(b,t)
    context.update({'comments': comments })


    return context


def get_default_blank_context(user):
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    community = get_community(user)

    context = {\
               'communities': Community.objects.all(),\
              'community': community,\
              'user_sorts':user_tags,\
            'top_sorts':top_tags,\
             'tags': Tag.objects.all(),\
             'questions': HardTag.objects.all(),\
            'all_sorts':get_all_sorts(4),\
            'location_term':community }   
    return context     

def get_default_bus_context(b,user):
    comments = get_business_comments(b)
    bus_tags = get_tags_business(b,user=user,q="")
        
        
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    hard_tags = get_hard_tags(b)
    
    pages = get_pages(b,bus_tags)
    b = get_single_bus_data(b,user)
    context = {}
    context.update({
        'business' : b,
        'comments': comments, 
        'lat':b.lat,
        'lng':b.lon,  
        'bus_tags':bus_tags, 
        'pages': pages, 
        'master_summary': get_master_summary_tag(),
        'tags': Tag.objects.all().order_by('-descr').reverse(),
        'user_sorts':user_tags,
        'top_sorts':top_tags,
        'all_sorts':get_all_sorts(4),
        'hard_tags':hard_tags,
        'location_term':get_community(user) ,
        'communities': Community.objects.all(),
        'following_business': is_user_subscribed(b,user),
         'feed' : get_bus_recent_activity(b),
        'bus_photos': get_all_bus_photos(b)
        })

    return context

def get_unauthenticated_context():
    top_tags = get_top_tags(10)
    context = { \
            'top_sorts':top_tags,\
            'all_sorts':get_all_sorts(4),\
            'location_term':get_community(None)\
            }
    return context


################################################################


def recurse_comments(comment,cur_list,even):
    cur_list.append(comment)
    replies = Comment.objects.filter(reply_to=comment).order_by('-date')
    for c in replies:
        if even:
            cur_list.append("open-even")
        else:
            cur_list.append("open-odd")
        recurse_comments(c,cur_list,not even)
        cur_list.append("close")


def get_tag_comments(b,tag):
    logger.debug('get for'+str(b)+ ' and tag ' + str(tag.descr))
    tagcomments = TagComment.objects.filter(business=b,tag=tag).order_by('-date')

    comment_list = []
    for tc in tagcomments:
        if tc.thread.reply_to is None: #root tag comment
            comment_list.append("open-even")
            recurse_comments(tc.thread,comment_list,False)
            comment_list.append("close")    
    results = []              
    for c in comment_list:
        if c != "open-even" and c != "open-odd" and c != "close":
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


def get_business_comments(business,user=False):
    buscomments = BusinessComment.objects.filter(business=business).order_by('-date')
    for bc in buscomments:
        print(bc.date)
    comment_list = []
    for bc in buscomments:
        if bc.thread.reply_to is None: #root tag comment
            comment_list.append("open-even")
            recurse_comments(bc.thread,comment_list,False)
            comment_list.append("close")    
    results = []              
    for c in comment_list:
        if c != "open-even" and c != "open-odd" and c != "close":
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
    context.update( {
        'search_term' : term,
        'business_list' : businesses,
        'nonempty' : True,
        'all_businesses' : businesses,
        'page_template': "ratings/listing/entry.html",
    } )
    return render_to_response('ratings/sort.html',  context_instance=RequestContext(request,context))


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

        context.update( {
            'community_businesses' : community_businesses,
            'your_businesses' : your_businesses,
            'all_businesses': all_businesses,
            'feed' : get_all_recent_activity(),
            'your_businesses' : your_businesses,
            'community_businesses' : community_businesses,
            'nonempty' : True,
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

@page_template("ratings/listing/entry.html") # just add this decorator
def display_tag(request,tag_id,extra_context=None):
    print('asdasdasdasd')
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

 
#I don't see why this cant be refactored... o well
def get_comment_by_id(cid):
    return Comment.objects.get(id=cid)

@csrf_exempt
def bus_details(request, bus_id):
    b = get_object_or_404(Business, pk=bus_id)
    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE
    
    context = get_default_bus_context(b, request.user)
    
    return render_to_response('ratings/busdetail.html', context_instance=RequestContext(request,context))


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
            return redirect(bus_details, bus_id=bus_id)
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
            return redirect(bus_details, bus_id=bus_id)
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
    context.update({'form':wiki_edit_form,
                    'page': page,
                    'tag' :t })
    
    
    return render_to_response('ratings/busdetail.html',
        RequestContext(request, context))
    
def user_details(request,uid):
    if not request.user.is_authenticated():
        return redirect('/')
  
    context = get_default_blank_context(request.user)
    checkon = User.objects.get(id=uid)
        
    communities = []
    for um in UserMembership.objects.filter(user=request.user):
        communities.append(um.community)

    context.update({
        'user_communities':communities,
        'user_favorites' : get_user_favorites(request.user),
        'user_traits' : get_user_traits(request.user),
        'checkon' : checkon,
        'feed' : get_user_recent_activity( checkon),
        'p' : get_user_profile_pic(checkon)
        })
    return render_to_response('ratings/user/user_detail.html', context_instance=RequestContext(request,context))
    
    
def add_trait(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
        
    #post a question 
    if request.method=='POST':

        form = TraitForm(request.POST)
        name = form.data['name'] 
        descr = form.data['descr']  
        
        if (Trait.objects.filter(creator=request.user,name=name,descr=descr).count() == 0):
            Trait.objects.create(creator=request.user,name=name,descr=descr)

    f = TraitForm()
    context = get_default_blank_context(request.user)
    context['form'] = f
    context['type'] = 'trait'
    context['traits'] = Trait.objects.all()
    return render_to_response('ratings/contribute/add_content.html', context, context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


