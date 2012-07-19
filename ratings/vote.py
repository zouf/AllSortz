'''
Created on May 29, 2012

@author: zouf
'''
from allsortz.views import get_comment_by_id
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business, Rating, CommentRating
from ratings.utility import get_single_bus_data
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
            business = Business.objects.get(id=request.POST['id'])
        except Business.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        if request.POST['type'] == 'up':
            rat = 5  # rating.rating + 1
            res = 'pos'
        else:
            rat = 1  # rating.rating - 1
            res = 'neg'

        try:
            rating = Rating.objects.get(business=business, user=request.user)
        except Rating.DoesNotExist:
            logger.debug("In vote create a new rating!")
            rating = Rating.objects.create(business=business, user=request.user, rating=rat)
        else:
            sys.stderr.write("rating already exists :(")
            return HttpResponse("{'success': 'false'}")
        rating.save()
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        response_data['pos_rating'] = getNumPosRatings(business)
        response_data['neg_rating'] = getNumNegRatings(business)
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')


@csrf_exempt
def comment_vote(request):

    logger.debug('in comment_vote')
    if request.method == 'POST':
        try:
            comment = get_comment_by_id(request.POST['id'])
        except:
            return HttpResponse("{'success': 'false'}")

        if request.POST['type'] == 'up':
            rat = 5  # rating.rating + 1
            res = 'pos'
        else:
            rat = 1  # rating.rating - 1
            res = 'neg'
        
        try:
            rating = CommentRating.objects.get(comment=comment, user=request.user)
        except CommentRating.DoesNotExist:
            logger.debug("In vote create a new comment rating!")
            rating = CommentRating.objects.create(comment=comment, user=request.user, rating=rat)
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
        
        rating.save()
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        response_data['pos_rating'] = getNumPosRatings(comment)
        response_data['neg_rating'] = getNumNegRatings(comment)
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')





@csrf_exempt
def remove_comment_vote(request):
    logger.debug('Remove Comment Vote!')
    if request.method == 'POST':
        try:
            comment = get_comment_by_id(request.POST['id']) 
        except:
            logger.debug("Comment does not exist")
            return HttpResponse("{'success': 'false'}")

        try:
            rating = CommentRating.objects.filter(comment=comment, user=request.user)
        except CommentRating.DoesNotExist:
            logger.debug("Comment does not exist")
            pass
        else:
            logger.debug("Deleting a comment rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(comment)
        response_data['neg_rating'] = getNumNegRatings(comment)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')




#from stack overflow
@csrf_exempt
def remove_vote(request):
    if request.method == 'POST':
        try:
            business = Business.objects.get(id=request.POST['id'])
        except Business.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        try:
            rating = Rating.objects.filter(business=business, user=request.user)
        except Rating.DoesNotExist:
            pass
        else:
            logger.debug("Deleting a rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(business)
        response_data['neg_rating'] = getNumNegRatings(business)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')
    
def add_bus_rating(request):
    if request.method == 'POST':
        try:
            business = Business.objects.get(id=request.POST['bid'])
        except Business.DoesNotExist:
            print("bus does not exist!")
            return HttpResponse("{'success': 'false'}")
        
        
        rat =  request.POST['rating'] 
        try:
            rating = Rating.objects.get(business=business, user=request.user)
        except Rating.DoesNotExist:
            logger.debug("In vote create a new rating!")
            rating = Rating(business=business, user=request.user, rating=rat)
        else:
            Rating.objects.filter(business=business,user=request.user).delete()
            rating = Rating(business=business, user=request.user, rating=rat)

        rating.save()
        response_data = dict()
        response_data['bid'] = str(request.POST['bid'])
        response_data['success'] = 'true'
        response_data['rating'] = rat
        context = {}
        business.rating = rating.rating
        context['business'] = get_single_bus_data(business,request.user)
        return render_to_response('ratings/listing/rate_data.html',context)
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')

                
