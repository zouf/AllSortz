'''
Created on Jun 12, 2012

@author: zouf
'''
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, TagRating
import logging

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
        tags = get_tags(b)
        return render_to_response('ratings/tags.html', {'business':b, 'tags': tags})
    

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
