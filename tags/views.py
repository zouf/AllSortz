'''
Created on Jun 12, 2012

@author: zouf
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business, Comment, PageRelationship
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, TagRating, CommentTag, UserTag
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
def add_tag(request):
    if request.method == 'POST':  # add a tag!
        form = request.POST
        nm = form['tag']
        logger.debug('Create a tag '+str(nm))
        bid = form['bid']
        b = Business.objects.get(id=bid)
        keyset = Tag.objects.filter(descr=nm, business=b)
        if(keyset.count() == 0):
            k = Tag.objects.create(descr=nm,creator=request.user,business=b)
            k.save()
            #create a wiki page
            pg = Page(name=nm)
            pg.save()
            
            pgr = PageRelationship(business=b,page=pg,tag=k)
            pgr.save()
        
        tags = get_tags(b)
        
   
        return render_to_response('ratings/tags.html', {'business':b, 'tags': tags})
    
    
@csrf_exempt
def add_user_tag(request):
    if request.method == 'POST':  # add a tag!
        form = request.POST
        nm = form['tag']
        logger.debug('Create a tag '+str(nm))
        bid = form['bid']
        b = Business.objects.get(id=bid)
        keyset = Tag.objects.filter(descr=nm, business=b)
        if(keyset.count() == 0):
            k = Tag.objects.create(descr=nm,creator=request.user,business=b)
            k.save()
        else:
            k = Tag.objects.get(descr=nm)
        
        
        UserTag.objects.create(tag=k,)
      
      
        
        tags = get_tags_user(request.user)
        
   
        return render_to_response('ratings/user/tags.html', {'uesr':request.user, 'tags': tags})
    

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
            relationship = PageRelationship.objects.get(business=business,tag=t)
            pages.append(relationship.page)
        except:
            logger.debug('error in getting relationships')
       
            
    return pages


def get_tags_user(user,q=""):
    if q != "":
        usertags = UserTag.objects.filter(descr__icontains=q)[:20]
    else:
        usertags = UserTag.objects.filter(user=user).order_by('-date')
    results = []
    for ut in usertags:
        results.append(ut)
    return results


def get_tags(b,user=False,q=""):
    if q != "":
        tags = Tag.objects.filter(descr__icontains=q)[:20]
    else:
        tags = Tag.objects.filter(business=b).order_by('-date')
    results = []
    for t in tags:
        try:
            rat =  TagRating.objects.get(tag=t)
            t.this_rat = rat.rating
            t.pos_ratings = getNumPosRatings(t)
            t.neg_ratings = getNumNegRatings(t)
        except:
            t.this_rat = 0
            t.pos_ratings = 0
            t.neg_ratings = 0
        results.append(t)
    results.sort(cmp=tag_comp)
    return results
