'''
Created on Jun 12, 2012

@author: zouf
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business, Comment, PageRelationship
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, TagRating, CommentTag, UserTag, BusinessTag
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
def add_tag_business(request):
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
            
        
        try: 
            bustag = BusinessTag.objects.get(tag=tag,business=b)
        except:
            bustag = BusinessTag.objects.create(tag=tag,business=b,creator=request.user)
            
            pg = Page(name=nm)
            pg.save()
            print('creating a page)')
            pgr = PageRelationship(business=b,page=pg,tag=bustag)
            pgr.save()
            print('page done')
        bus_tags = get_tags_business(b)
        
   
        return render_to_response('ratings/tags.html', {'business':b, 'bus_tags': bus_tags, 'tags':Tag.objects.all()})
    
    
@csrf_exempt
def add_user_tag(request):
    u = request.user
    if request.method == 'POST':  # add a tag!
        form = request.POST
        nm = form['tag']
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
        return render_to_response('ratings/user/tags.html', {'user':request.user, 'tags': tags, 'user_sorts': user_tags})

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
            relationship = PageRelationship.objects.get(business=business,tag=bt)
            pages.append(relationship.page)
        except:
            logger.debug('error in getting relationships')
            print('error in getitng pages)')
          
  
    print("pages are "+str(pages)) 
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
