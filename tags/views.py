'''
Created on Jun 12, 2012

@author: zouf
'''
from communities.models import UserMembership
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business, Comment, PageRelationship, Community, \
    UserFavorite
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, TagRating, CommentTag, UserTag, BusinessTag, \
    BooleanQuestion, HardTag
from usertraits.models import TraitRelationship
from wiki.models import Page
import json
import logging
import sys

logger = logging.getLogger(__name__)
    
#sorts tags
def tag_comp(x,y):
    #eventually do something more intelligent here!
    xTot = x.pos_ratings - x.neg_ratings
    yTot = y.pos_ratings - y.neg_ratings
    if (xTot > yTot):
        return -1
    elif (xTot < yTot ):
        return 1
    else:
        return 0
    
@csrf_exempt
def add_a_sort(request):
    print ('in add a sort')
    if request.method == 'POST':  # add a tag!
        form = request.POST
        nm = form['descr']
        try:
            tag = Tag.objects.get(descr=nm)
        except:
            tag = Tag.objects.create(descr=nm,creator=request.user)
        return render_to_response('ratings/contribute/sortlist.html', {'tags':Tag.objects.all()})
    
    
    
@csrf_exempt
def add_tag_business(request):
    print ('here')
    if request.method == 'POST':  # add a tag!
        form = request.POST
        nm = form['tag']
        logger.debug('Create a tag '+str(nm))
        bid = form['bid']
            
        b = Business.objects.get(id=bid)
        try:
            tag = Tag.objects.get(descr=nm)
        except:
            tag = Tag.objects.create(descr=nm,creator=request.user)
            
        print(tag)
        try: 
            bustag = BusinessTag.objects.get(tag=tag,business=b)
        except:
            bustag = BusinessTag.objects.create(tag=tag,business=b,creator=request.user)
        print(bustag)
        try:
            pg = Page.objects.get(name=nm)
        except:
            pg = Page(name=nm)
            pg.save()
        print('creating a page)')
        print(tag)
        pgr = PageRelationship(business=b,page=pg,tag=bustag.tag)
        pgr.save()
        print('page done')
        bus_tags = get_tags_business(b)
        
   
        return render_to_response('ratings/sorts.html', {'business':b, 'bus_tags': bus_tags, 'tags':Tag.objects.all()})
    
    
#Right now I'm trying to completely refactor this function to ahndle all user subscriptions
@csrf_exempt
def add_user_tag(request):
    u = request.user
    if request.method == 'POST':  # add a tag!
        form = request.POST

        if form['type']  == 'tag':
            nm = form['data']
            print("TAGAGATAT")
            logger.debug('Create a User tag '+str(nm))
            try:
                tag = Tag.objects.get(descr=nm)
            except:
                tag = Tag.objects.create(descr=nm,creator=request.user)
            try: 
                UserTag.objects.get(tag=tag,user=u)
            except:
                UserTag.objects.create(tag=tag,user=u)
            user_tags = get_tags_user(u)
            tags = Tag.objects.all()
            print(user_tags)
            return render_to_response('ratings/sorts.html', {'user':request.user, 'tags': tags, 'user_sorts': user_tags})
        elif form['type']=="comm": #associate a user with a community
            nm = form['data']
            logger.debug('Create a User tag '+str(nm))
            try:
                community = Community.objects.get(name=nm)
            except:
                logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                
            if UserMembership.objects.filter().count() == 0:
                UserMembership.objects.create(community=community,user=u,logged_in=False)
           
            response_data = dict()
            response_data['success'] = 'true'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        elif form['type']=="bid": #associate a user with a community
            bid = form['data']
            print('add favorite!')

            try:
                business = Business.objects.get(id=bid)
            except:
                print('error')
                logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                
            if UserFavorite.objects.filter(business=business,user=u).count() > 0:
                print('create a favorite')
                UserFavorite.objects.filter(business=business,user=u).delete()
            UserFavorite.objects.create(business=business,user=u)
           
           
            response_data = dict()
            response_data['success'] = 'true'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")


@csrf_exempt
def remove_user_tag(request):
    u = request.user
    if request.method == 'POST':  # add a tag!
        form = request.POST
        print(form)
        print('delete a tag in form')
        if form['type']  == 'tag':
            nm = form['data']
            logger.debug('delete a User tag '+str(nm))
            try:
                tag = Tag.objects.get(descr=nm)
                UserTag.objects.filter(tag=tag,user=u).delete()
            except: 
                print('exception goddamit')
                logger.error("trying to delete a user tag hat wasn't there")
                
            response_data = dict()
            response_data['success'] = 'true'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        elif form['type']=="comm": #associate a user with a community
            nm = form['data']
            logger.debug('delete a community relationship '+str(nm))
            try:
                community = Community.objects.get(name=nm)  
                UserMembership.objects.filter(community=community,user=u).delete()
            except:
                logger.error("trying to delete a relationship with a community that wasn't there")
    
            response_data = dict()
            response_data['success'] = 'true'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")

        elif form['type']=="bid": #associate a user with a community
            bid = form['data']
            try:
                business = Business.objects.get(id=bid)  
                UserFavorite.objects.filter(business=business,user=u).delete()
            except:
                logger.error("trying to delete a relationship with a community that wasn't there")
    
            response_data = dict()
            response_data['success'] = 'true'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")



def get_top_tags(N):
    tags = Tag.objects.filter()[:N]
    return tags


def get_all_sorts(N):
    tags = Tag.objects.all()
    i = 0
    sorts = []
    for t in tags:
        if i %N == 0:
            if i != 0:
                sorts.append("close") 
            sorts.append("open")
        sorts.append(t)
        i += 1
    return sorts

#this funciton is for autocomplete on tags
def get_all_tags(request):
    if request.method == 'GET':
        q = request.GET.get('term', '')
        tags = Tag.objects.filter(descr__icontains=q)[:20]
        results = []
        for tag in tags:
            print(tag.descr)
            results.append(tag.descr)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)

#get pages for the wiki style entry
def get_pages(business,tags):
    pages = []
    for t in tags:
       
        try:
            bt = BusinessTag.objects.get(business=business,tag=t)
            print(bt)
            relationship = PageRelationship.objects.get(business=business,tag=bt.tag)
            pages.append(relationship.page)
        except MultipleObjectsReturned:
            #logger.error('Multiple Pages returned in '+str(__name__))
            #XXX 
            relationship = PageRelationship.objects.filter(business=business,tag=bt.tag)[0]
            pages.append(relationship.page)
  
    return pages


def get_tags_user(user,q=""):
    #bustags = BusinessTag.objects.filter(descr__icontains=q)[:20]
    usertags = UserTag.objects.filter(user=user)
    tags = []
    for ut in usertags:
        tags.append(ut.tag)
    return tags


def get_tags_business(b,user=False,q=""):
    #bustags = BusinessTag.objects.filter(descr__icontains=q)[:20]
    bustags = BusinessTag.objects.filter(business=b)
    tags = []
    for bt in bustags:
        tags.append(bt.tag)
    return tags


def get_questions(b,user):
    if b is None:
        return HardTag.objects.all()
    hardtags = HardTag.objects.all()
    results = []
    for ht in hardtags:
        qset = BooleanQuestion.objects.filter(hardtag=ht,business=b,user=user)
        if qset.count() < 1: # has not been answered
            results.append(ht)
        
    return results
        

def get_hard_tags(b):
    hardtags = HardTag.objects.all()
    results = []
    for ht in hardtags:
        PosAnswers = BooleanQuestion.objects.filter(hardtag=ht,business=b,agree=True)
        TotAnswers = BooleanQuestion.objects.filter(hardtag=ht,business=b)
        
        PosAnswers = PosAnswers.aggregate(Count('hardtag'))
        TotAnswers = TotAnswers.aggregate(Count('hardtag'))
        
        numPos = PosAnswers['hardtag__count']
        numTot = TotAnswers['hardtag__count']
        
        if numTot != 0:
            if numPos / numTot > 0.5:
                ans = True
            else:
                ans = False
   
            ques = dict()
            ques['question'] = ht.question
            ques['answer'] = ans
            results.append(ques)
    return results

