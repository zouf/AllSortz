'''
Created on Jun 12, 2012

@author: zouf
'''
from django.shortcuts import render_to_response
from ratings.models import Business, Tip, TipRating
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import logging
import sys


logger = logging.getLogger(__name__)

#sorts tips
def tip_comp(x,y):
    #eventually do something more intelligent here!
    xTot = x.pos_ratings - x.neg_ratings
    yTot = y.pos_ratings - y.neg_ratings
    if (xTot > yTot):
        return -1
    elif (xTot < yTot ):
        return 1
    else:
        return 0


#adds tips to the database
def add_tip(request):
    if request.method == 'POST':  # add a tip!
       
        form = request.POST

        nm = form['tip']
        bid = form['bid']
        b = Business.objects.get(id=bid)
        #don't readd a tip if its identical
        keyset = Tip.objects.filter(descr=nm, business=b)
        if(keyset.count() == 0):
            try:
                k = Tip.objects.create(descr=nm,user=request.user,business=b)
            except:
                logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            k.save()
        tips = get_tips(b)
        return render_to_response('ratings/tips.html', {'business':b, 'tips': tips})


def get_tips(b,user=False,q=""):
    if q != "":
        tips = Tip.objects.filter(descr__icontains=q)[:20]
    else:
        tips = Tip.objects.filter(business=b).order_by('-date')
    results = []
    for t in tips:
        try:
            rat =  TipRating.objects.get(tip=t)
            t.this_rat = rat.rating
            t.pos_ratings = getNumPosRatings(t)
            t.neg_ratings = getNumNegRatings(t)
        except:
            t.this_rat = 0
            t.pos_ratings = 0
            t.neg_ratings = 0
        results.append(t)

    results.sort(cmp=tip_comp)
    return results
        