'''
Created on Jun 13, 2012

@author: zouf
'''
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, TagRating, BusinessTag
import json
import logging
import sys



logger = logging.getLogger(__name__)




@csrf_exempt
def tag_vote(request):
    logger.debug('tag_vote')
    if request.method == 'POST':
        try:
            tag = BusinessTag.objects.get(id=request.POST['id'])
        except Tag.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        if request.POST['type'] == 'up':
            rat = 5  # rating.rating + 1
            res = 'pos'
        else:
            rat = 1  # rating.rating - 1
            res = 'neg'
        try:
            rating = TagRating.objects.get(tag=tag, user=request.user)
        except TagRating.DoesNotExist:
            logger.debug("In tag vote create a new tag rating!")
            rating = TagRating.objects.create(tag=tag, user=request.user, rating=rat)
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
        else:
            logger.debug("Tag rating already exists :(")
            return HttpResponse("{'success': 'false'}")
        rating.save()
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        response_data['pos_rating'] = getNumPosRatings(tag)
        response_data['neg_rating'] = getNumNegRatings(tag)
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        logger.debug("404 raised in tag_vote")
        raise Http404('What are you doing here?')


@csrf_exempt
def remove_tag_vote(request):
    logger.debug('Remove Tag Vote!')
    if request.method == 'POST':
        try:
            tag = BusinessTag.objects.get(id=request.POST['id'])
        except Tag.DoesNotExist:
            logger.debug("Tag does not exist")
            return HttpResponse("{'success': 'false'}")

        try:
            rating = TagRating.objects.filter(tag=tag, user=request.user)
        except TagRating.DoesNotExist:
            logger.debug("Tag does not exist")
            pass
        else:
            logger.debug("Deleting a tag rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(tag)
        response_data['neg_rating'] = getNumNegRatings(tag)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')


