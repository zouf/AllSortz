'''
Created on May 29, 2012

@author: zouf
'''
from comments.models import Comment, CommentRating
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import json
import logging
import sys



logger = logging.getLogger(__name__)


@csrf_exempt
def comment_vote(request):
    print('in comment vote')
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


