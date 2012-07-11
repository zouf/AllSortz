from communities.models import BusinessMembership, UserMembership
from communities.views import get_default
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from endless_pagination.decorators import page_template
from photos.views import get_photo_web_url
from ratings.contexts import get_tag_comments, get_business_comments, \
    get_default_blank_context, get_default_tag_context, get_default_bus_context, \
    get_unauthenticated_context
from ratings.favorite import get_user_favorites, is_user_subscribed
from ratings.feed import  get_all_recent_activity, \
    get_user_recent_activity
from ratings.models import Business, Comment, TagComment, PageRelationship, \
    BusinessComment
from ratings.search import search_site
from ratings.utility import get_bus_data, \
    get_businesses_by_tag, get_businesses_by_community, get_businesses_trending, \
    get_businesses_by_your
from recommendation.recengine import RecEngine
from tags.form import TagForm
from tags.models import Tag, UserTag
from usertraits.views import get_user_traits
from wiki.forms import PageForm
from wiki.models import Page
import logging





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
    context.update( {
        'search_term' : term,
        'business_list' : businesses,
        'nonempty' : True,
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
    context['form']=wiki_edit_form
    context['page']=page
    context['tag'] =t 
    
    for tc in context['comments']:
        print(tc)
    
    
    return render_to_response('ratings/busdetail.html',
        RequestContext(request, context))



@csrf_exempt
def bus_details(request, bus_id):
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
    context['type'] = 'tag'   
    return render_to_response('ratings/contribute/add_content.html',context, context_instance=RequestContext(request))


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
 

def user_details(request,uid):
    if not request.user.is_authenticated():
        return redirect(index)
  
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
        'feed' : get_user_recent_activity(checkon)
        })
    return render_to_response('ratings/user/user_detail.html', context_instance=RequestContext(request,context))
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


