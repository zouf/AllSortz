'''
Created on May 29, 2012

@author: zouf
'''
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business, Rating, Comment, CommentRating
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import json
import logging
import sys



logger = logging.getLogger(__name__)


#@csrf_exempt
#def tip_vote(request):
#    logger.debug('in tip_vote')
#    if request.method == 'POST':
#        try:
#            tip = Tip.objects.get(id=request.POST['id'])
#        except Tip.DoesNotExist:
#            return HttpResponse("{'success': 'false'}")
#
#        if request.POST['type'] == 'up':
#            rat = 5  # rating.rating + 1
#            res = 'pos'
#        else:
#            rat = 1  # rating.rating - 1
#            res = 'neg'
#        try:
#            rating = TipRating.objects.get(tip=tip, user=request.user)
#        except TipRating.DoesNotExist:
#            logger.debug("In vote create a new tip rating!")
#            rating = TipRating.objects.create(tip=tip, user=request.user, rating=rat)
#        except:
#            logger.debug("Unexpected error:", sys.exc_info()[0])
#        else:
#            logger.debug("tip vote already exists :(")
#            return HttpResponse("{'success': 'false'}")
#
#        rating.save()
#        response_data = dict()
#        response_data['id'] = str(request.POST['id'])
#        response_data['success'] = 'true'
#        response_data['rating'] = res
#        response_data['pos_rating'] = getNumPosRatings(tip)
#        response_data['neg_rating'] = getNumNegRatings(tip)
#        return HttpResponse(json.dumps(response_data), mimetype="application/json")
#        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
#    else:
#        raise Http404('What are you doing here?')



@csrf_exempt
def vote(request):
    if request.method == 'POST':
        vote_on = request.POST['id']
        print(vote_on)
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
            rating = Rating.objects.get(business=business, username=request.user)
        except Rating.DoesNotExist:
            logger.debug("In vote create a new rating!")
            rating = Rating.objects.create(business=business, username=request.user, rating=rat)
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
            comment = Comment.objects.get(id=request.POST['id'])
        except Comment.DoesNotExist:
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
            comment = Comment.objects.get(id=request.POST['id'])
        except Comment.DoesNotExist:
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
            rating = Rating.objects.filter(business=business, username=request.user)
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
