'''
Created on Jun 18, 2012

@author: zouf
'''
from activities.models import Activity, ActRating
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Rating
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import json
import logging
import sys
logger = logging.getLogger(__name__)

@csrf_exempt
def vote(request):
    if request.method == 'POST':
        vote_on = request.POST['id']
        try:
            activity = Activity.objects.get(id=request.POST['id'])
        except Activity.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        if request.POST['type'] == 'up':
            rat = 5  # rating.rating + 1
            res = 'pos'
        else:
            rat = 1  # rating.rating - 1
            res = 'neg'

        try:
            rating = ActRating.objects.get(activity=activity, user=request.user)
        except ActRating.DoesNotExist:
            logger.debug("In vote create a new rating!")
            rating = ActRating.objects.create(activity=activity, user=request.user, rating=rat)
        else:
            sys.stderr.write("rating already exists :(")
            return HttpResponse("{'success': 'false'}")
        rating.save()
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        response_data['pos_rating'] = getNumPosRatings(activity)
        response_data['neg_rating'] = getNumNegRatings(activity)
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')

#
#@csrf_exempt
#def remove_tip_vote(request):
#    logger.debug('Remove Tip Vote!')
#    if request.method == 'POST':
#        try:
#            tip = Tip.objects.get(id=request.POST['id'])
#        except Tip.DoesNotExist:
#            logger.debug("Tip does not exist")
#            return HttpResponse("{'success': 'false'}")
#
#        try:
#            rating = TipRating.objects.filter(tip=tip, user=request.user)
#        except TipRating.DoesNotExist:
#            logger.debug("Tip does not exist")
#            pass
#        else:
#            logger.debug("Deleting a tip rating")
#            rating.delete()
#
#        response_data = dict()
#        response_data['id'] = str(request.POST['id'])
#        response_data['success'] = 'true'
#        response_data['pos_rating'] = getNumPosRatings(tip)
#        response_data['neg_rating'] = getNumNegRatings(tip)
#
#        return HttpResponse(json.dumps(response_data), mimetype="application/json")
#    else:
#        raise Http404('What are you doing here?')




#from stack overflow
@csrf_exempt
def remove_vote(request):
    if request.method == 'POST':
        try:
            activity = Activity.objects.get(id=request.POST['id'])
        except Activity.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        try:
            rating = ActRating.objects.filter(activity=activity, user=request.user)
        except ActRating.DoesNotExist:
            pass
        else:
            logger.debug("Deleting a actrating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(activity)
        response_data['neg_rating'] = getNumNegRatings(activity)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')
