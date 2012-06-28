from communities.forms import CommunityForm
from communities.models import BusinessMembership
from communities.views import get_community, get_default
from django.contrib.auth import logout
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from photos.models import BusinessPhoto
from photos.views import get_photo_web_url
from ratings.forms import BusinessForm, CommentForm
from ratings.models import Business, Comment, CommentRating, TagComment, \
    PageRelationship, BusinessComment, Community
from ratings.populate import create_business
from ratings.search import search_site
from ratings.utility import get_lat, get_bus_data, get_single_bus_data
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from recommendation.recengine import RecEngine
from tags.form import HardTagForm, TagForm
from tags.models import CommentTag, Tag, BusinessTag, UserTag, HardTag, \
    BooleanQuestion
from tags.views import get_tags_business, get_pages, get_tags_user, get_top_tags, \
    get_all_sorts, get_hard_tags, get_questions
from wiki.forms import PageForm
from wiki.models import Page
import logging
import sys




logger = logging.getLogger(__name__)

re = RecEngine()



def get_default_tag_context(b,t,user):
    comments = get_tag_comments(b,t)
    bus_tags = get_tags_business(b,user=user,q="")
        
        
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    hard_tags = get_hard_tags(b)
    
    pages = get_pages(b,bus_tags)
    latlng = get_lat(b.address + " " + b.city + ", " + b.state)
    b = get_single_bus_data(b,user)
    

    
    context =   { \
        'business' : b, \
        'comments': comments, \
        'lat': latlng[0],\
        'lng':latlng[1],  \
        'bus_tags':bus_tags, \
        'pages': pages, \
        'tags': Tag.objects.all(),\
        'user_sorts':user_tags,\
        'top_sorts':top_tags,\
        'all_sorts':get_all_sorts(4),\
        'hard_tags':hard_tags,\
        'location_term':get_community(user)
        }

    return context


def get_default_blank_context(user):
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    community = get_community(user)

    context = {\
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
    latlng = get_lat(b.address + " " + b.city + ", " + b.state)
    b = get_single_bus_data(b,user)
    context =   { \
        'business' : b, \
        'comments': comments, \
        'lat': latlng[0],\
        'lng':latlng[1],  \
        'bus_tags':bus_tags, \
        'pages': pages, \
        'tags': Tag.objects.all(),\
        'user_sorts':user_tags,\
        'top_sorts':top_tags,\
        'all_sorts':get_all_sorts(4),\
        'hard_tags':hard_tags,\
        'location_term':get_community(user)
        }

    return context

def get_unauthenticated_context():
    top_tags = get_top_tags(10)
    context = { \
            'top_sorts':top_tags,\
            'all_sorts':get_all_sorts(4),\
            'location_term':get_community(None)
            }
    return context

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






def get_business_comments(business,user=False):
    buscomments = BusinessComment.objects.filter(business=business).order_by('-date').reverse()
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
    print('return bus comments')
    return results

def get_tag_comments(b,tag):
    print('get for'+str(b)+ ' and tag ' + str(tag.descr))
    tagcomments = TagComment.objects.filter(business=b,tag=tag).order_by('-date').reverse()

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


#gets all the comments, including nested ones
#adds tokens "open" and "close" to denote subcomments
def get_comments(b,user=False,q=""):
    if q != "":
        comments = Comment.objects.filter(descr__icontains=q)[:20].order_by('-date')
    else:
        comments = Comment.objects.filter(business=b).order_by('-date')
    
  
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
#@csrf_exempt
#def add_comment(request):
#    logger.debug('in add comment')
#    print('in add comment regular')
#    if request.method == 'POST':  # add a comment!
#        form = request.POST       
#        print(form)
#        #base comment submission
#        if 'cid' not in form:   
#            print(form)   
#            nm = form['comment']
#            bid = form['bid']
#            b = Business.objects.get(id=bid)
#            keyset = Comment.objects.filter(descr=nm, business=b)
#            if(keyset.count() == 0):
#                try:
#                    k = Comment.objects.create(descr=nm,user=request.user,business=b,reply_to=None)
#                except:
#                    logger.error("Unexpected error:" + str(sys.exc_info()[0]))
#                k.save()
#        else:  #reply to another comment submission
#            nm = form['comment']
#            bid = form['bid']
#            print(form)
#            b = Business.objects.get(id=bid)
#            cid = form['cid']
#            c = Comment.objects.get(id=cid)
#            keyset = Comment.objects.filter(descr=nm, business=b)
#            if(keyset.count() == 0):
#                try:
#                    k = Comment.objects.create(descr=nm,user=request.user,reply_to=c)
#                except:
#                    logger.error("Unexpected error:" + str(sys.exc_info()[0]))
#                k.save()
#        comment_list = get_business_comments(b,request.user)
#
#        return render_to_response('ratings/discussion/thread.html', {'business':b, 'comments': comment_list})



@csrf_exempt
def add_tag_comment(request):
    logger.debug('in add comment')
    print('in add comments)')
    if request.method == 'POST':  # add a comment!
        form = request.POST 
        print(form)     
        #add a comment to a business' tag page 
        if 'tid'  in form:
            bid =form['bid']
            b = Business.objects.get(id=bid)
            tid = form['tid']
            t = Tag.objects.get(id=tid)
            print(form)
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
            return render_to_response('ratings/discussion/thread.html', {'tag':t, 'comments': comment_list})
        
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




def recurse_comments(comment,cur_list,even):
    cur_list.append(comment)
    replies = Comment.objects.filter(reply_to=comment).order_by('-date').reverse()
    for c in replies:
        if even:
            cur_list.append("open-even")
        else:
            cur_list.append("open-odd")
        recurse_comments(c,cur_list,not even)
        cur_list.append("close")



def coming_soon(request):
    if request.user.is_authenticated():
        return index(request)
    else:
        return render_to_response('coming_soon.html', context_instance=RequestContext(request))




def display_tag(request,tag_id):
    print('disp tag')
    t = get_object_or_404(Tag, pk=tag_id)
    businesses = get_businesses_by_tag(t,request.user, request.GET.get('page'))
    
    try:
        UserTag.objects.get(tag=t,user=request.user)
        subscribed=True
    except:
        subscribed=False

    context = get_default_blank_context(request.user)
    context['search_term'] = t.descr
    context['business_list'] = businesses
    context['subscribed'] = subscribed
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
    businesses = get_bus_data(business_list,request.user)
    paginator = Paginator(businesses, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        businesses = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        businesses = paginator.page(1)
    except EmptyPage:
        businesses = paginator.page(paginator.num_pages)
        

    context = get_default_blank_context(request.user)
    context['search_term'] = term
    context['business_list'] = businesses
    return render_to_response('ratings/sort.html',  context_instance=RequestContext(request,context))




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

def how_it_works(request):
    return render_to_response('how_it_works.html',context_instance=RequestContext(request))


@csrf_exempt
def detail_keywords(request, bus_id):
    b = get_object_or_404(Business, pk=bus_id)

    try:
        b.photourl = get_photo_web_url(b)
    except:
        b.photourl= "" #NONE
    
    context = get_default_bus_context(b, request.user)

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
    context['communities'] = Community.objects.all()            
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
    
    return render_to_response('ratings/contribute/add_content.html', context, context_instance=RequestContext(request))

def ans_business_questions(request,bus_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    if request.method != 'POST':
        b = get_object_or_404(Business, pk=bus_id)
        user_tags = get_tags_user(request.user,"")
        top_tags = get_top_tags(10)    
    
       
        latlng = get_lat(b.address + " " + b.city + ", " + b.state)
        try:
            b.photourl = get_photo_web_url(b)
        except:
            b.photourl= "" #NONE
        questions = get_questions(b,request.user)
        b = get_single_bus_data(b,request.user)
        
        if latlng:
            context =   { \
            'business' : b, \
            'lat': latlng[0],\
            'lng':latlng[1],  \
            'questions':questions,\
            'tags': Tag.objects.all(),\
            'user_sorts':user_tags,\
            'top_sorts':top_tags,\
            'all_sorts':get_all_sorts(4),\
            'location_term':get_community(request.user)
            }
    
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
        
        b = create_business(name, address, state, city, 1, 1)
        b.save()
        if 'image' in request.FILES:
            img = request.FILES['image']
            bp = BusinessPhoto(user=request.user, business=b, image=img, title="test main", caption="test cap")
            bp.save()
   
      
        
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
    else:  # Print a boring business form
        f = BusinessForm()
        user_tags = get_tags_user(request.user,"")
        top_tags = get_top_tags(10)    
        
        questions = get_questions(None,request.user)
        
        context = { 'form':f, \
                    'user_sorts':user_tags,\
                'top_sorts':top_tags,\
                'questions':questions,\
                'all_sorts':get_all_sorts(4),\
                'location_term':get_community(request.user) }
        
        return render_to_response('ratings/contribute/add_business.html', context, context_instance=RequestContext(request))



def paginate_businesses(business_list,page, num):
    paginator = Paginator(business_list, num)  # Show 25 contacts per page
    try:
        business_list = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        business_list = paginator.page(1)
    except EmptyPage:
        business_list = paginator.page(paginator.num_pages)
    return business_list


def get_businesses_by_community(user,page,checkForIntersection):
    alreadyThere = dict()
    for nt in checkForIntersection:
        alreadyThere[nt] = True
        
        
    community = get_community(user)
    businesses = []
    try:
        busMembership = BusinessMembership.objects.filter(community = community)
        for b in busMembership:
            if b not in alreadyThere:
                businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    print(businesses)
    business_list = get_bus_data(businesses,user)
    business_list = paginate_businesses(business_list,page,5)

    for b in business_list:
        bustags = BusinessTag.objects.filter(business=b)
        b.tags = []
        for bt in bustags:
            b.tags.append(bt.tag)

        
    return business_list

def get_businesses_trending(user,page,checkForIntersection):
    alreadyThere = dict()
    for nt in checkForIntersection:
        alreadyThere[nt] = True
        
    businesses = []
    try:
        allBus = Business.objects.all() # order by rating
        for b in allBus:
            if b not in alreadyThere:
                businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
        
        
    business_list = get_bus_data(businesses,user)
    business_list = paginate_businesses(business_list,page,5)

    for b in business_list:
        bustags = BusinessTag.objects.filter(business=b)
        b.tags = []
        for bt in bustags:
            b.tags.append(bt.tag)

    return business_list
        
        
def get_businesses_by_your(user,page,checkForIntersection):
    alreadyThere = dict()
    for nt in checkForIntersection:
        alreadyThere[nt] = True
        
    businesses = []
    try:
        allBus = Business.objects.all() # order by rating
        for b in allBus:
            if b not in alreadyThere:
                businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    business_list = get_bus_data(businesses,user)
    business_list = paginate_businesses(business_list,page,5)
    return business_list


def get_businesses_by_tag(t,user,page):
    bustags = BusinessTag.objects.filter(tag=t)
    businesses = []
    for bt in bustags:
        businesses.append(bt.business)    
    business_list = get_bus_data(businesses,user)
    business_list = paginate_businesses(business_list,page,5)
    return business_list

        
def index(request):
    if request.user.is_authenticated():
        current_businesses = []
        
       
        community_businesses = get_businesses_by_community(request.user,request.GET.get('page'),current_businesses)
        current_businesses+=community_businesses.object_list
        
        all_businesses = get_businesses_trending(request.user,request.GET.get('page'),current_businesses)
        current_businesses+=all_businesses.object_list

        your_businesses = get_businesses_by_your(request.user,request.GET.get('page'),current_businesses)
        current_businesses+=your_businesses.object_list

            
            
        context = get_default_blank_context(request.user)
        context['community_businesses'] = community_businesses
        context['your_businesses'] = your_businesses
        context['all_businesses'] = all_businesses
    
        return render_to_response('ratings/index.html', context_instance=RequestContext(request,context))
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

def user_details(request):
    if not request.user.is_authenticated():
        return redirect(index)
    
    user_tags = get_tags_user(request.user,"")
    top_tags = get_top_tags(10)

    context = {\
        'user': request.user,\
        'tags':Tag.objects.all(),\
         'top_sorts':top_tags,\
        'user_sorts': user_tags,\
        'all_sorts':get_all_sorts(4),\
        'location_term':get_community(request.user)
    }
    
    return render_to_response('ratings/user/user_detail.html', context_instance=RequestContext(request,context))
    


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


