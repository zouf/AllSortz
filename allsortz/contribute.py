'''
@author: zouf
'''
from allsortz.forms import BusinessForm
from allsortz.populate import create_business
from allsortz.views import get_default_bus_context, get_default_blank_context
from communities.forms import CommunityForm
from communities.models import BusinessMembership, Community
from communities.views import get_community
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from photos.views import get_photo_web_url, add_photo_by_upload
from ratings.models import Business
from ratings.utility import get_single_bus_data, get_lat
from tags.form import TagForm, HardTagForm
from tags.models import HardTag, BooleanQuestion, Tag, IntegerQuestion, ValueTag
from tags.views import get_questions, getValueTagsWithOptions
import logging


logger = logging.getLogger(__name__)


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
    context['value_questions'] = getValueTagsWithOptions()
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
        context['value_questions'] = getValueTagsWithOptions()
        print(context['value_questions'][0].options)
        return render_to_response('ratings/contribute/ans_questions.html', context_instance=RequestContext(request,context))
    else:
        
        bid = request.POST['bid']
        values = []   
        booleans = []
        #get the list of anwers
        for key in request.POST:
            if key.find('answer') > -1:
                booleans.append(request.POST[key])
        for key in request.POST:
            if key.find('values') > -1:
                values.append(request.POST[key])
                
        b = Business.objects.get(id=bid)
        
        for v in booleans:
            ans = v.split('_')[1]
            qid = v.split('_')[0]
            hardtag = HardTag.objects.get(id=qid)
            if ans == 'y':
                BooleanQuestion.objects.create(hardtag=hardtag,business = b,user=request.user,agree=True)
            else:
                BooleanQuestion.objects.create(hardtag=hardtag,business = b,user=request.user,agree=False) 
        
        
        for v in values:
            ans = v.split('_')[1]
            vid = v.split('_')[0]
            valuetag = ValueTag.objects.get(id=vid)
            IntegerQuestion.objects.create(valuetag=valuetag,business = b,user=request.user,value=ans) 
          
        return redirect('/ratings/'+str(bus_id)+'/')

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
            add_photo_by_upload(img,b,request.user,default=True)
   
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
        
        return redirect('/ratings/'+str(b.id)+'/')
    else:  # Print a  business form
        context = get_default_blank_context(request.user)
        context['questions'] = get_questions(None,request.user)
        context['form'] = BusinessForm()
        return render_to_response('ratings/contribute/add_business.html', context, context_instance=RequestContext(request))

