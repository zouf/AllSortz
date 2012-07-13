from allsortz.feed import get_user_recent_activity
from allsortz.views import get_default_bus_context, get_default_tag_context, \
    get_default_blank_context, bus_details
from communities.models import UserMembership
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from photos.views import get_photo_web_url
from ratings.favorite import get_user_favorites
from ratings.models import Business, PageRelationship
from tags.form import TagForm
from tags.models import Tag
from usertraits.views import get_user_traits
from wiki.forms import PageForm
from wiki.models import Page
import logging




logger = logging.getLogger(__name__)

#re = RecEngine() 






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
        'feed' : get_user_recent_activity( checkon)
        })
    return render_to_response('ratings/user/user_detail.html', context_instance=RequestContext(request,context))
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


