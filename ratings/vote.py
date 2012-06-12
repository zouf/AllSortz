'''
Created on May 29, 2012

@author: zouf
'''
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Tip, TipRating, Business, Rating, Tag, TagRating
from ratings.utility import log_msg
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import json
import sys


@csrf_exempt
def tip_vote(request):
    print   ('in tip_vote')
    if request.method == 'POST':
        try:
            tip = Tip.objects.get(id=request.POST['id'])
        except Tip.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        if request.POST['type'] == 'up':
            rat = 5  # rating.rating + 1
            res = 'pos'
        else:
            rat = 1  # rating.rating - 1
            res = 'neg'
            
        print('here')
        try:
            log_msg('get')
            rating = TipRating.objects.get(tip=tip, user=request.user)
            print('after get')
        except TipRating.DoesNotExist:
            log_msg("In vote create a new tip rating!")
            rating = TipRating.objects.create(tip=tip, user=request.user, rating=rat)
        except:
            log_msg("Unexpected error:", sys.exc_info()[0])
        else:
            log_msg("tip vote already exists :(")
            return HttpResponse("{'success': 'false'}")

        rating.save()
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        response_data['pos_rating'] = getNumPosRatings(tip)
        response_data['neg_rating'] = getNumNegRatings(tip)
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')




@csrf_exempt
def tag_vote(request):
    print('tag_vote')
    if request.method == 'POST':
        try:
            tag = Tag.objects.get(id=request.POST['id'])
        except Tag.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        if request.POST['type'] == 'up':
            rat = 5  # rating.rating + 1
            res = 'pos'
        else:
            rat = 1  # rating.rating - 1
            res = 'neg'
        print('here in tag_vote')
        try:
            rating = TagRating.objects.get(tag=tag, user=request.user)
        except TagRating.DoesNotExist:
            print("In tag vote create a new tag rating!")
            rating = TagRating.objects.create(tag=tag, user=request.user, rating=rat)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        else:
            print("tag rating already exists :(")
            return HttpResponse("{'success': 'false'}")
        rating.save()
        print("after save")
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        response_data['pos_rating'] = getNumPosRatings(tag)
        response_data['neg_rating'] = getNumNegRatings(tag)
        print("before resp data")
        print(response_data)
        print("response data")
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')



@csrf_exempt
def vote(request):
    print('vote')
    if request.method == 'POST':
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
            log_msg("In vote create a new rating!")
            rating = Rating.objects.create(business=business, username=request.user, rating=rat)
        else:
            sys.stderr.write("rating already exists :(")
            return HttpResponse("{'success': 'false'}")
        rating.save()
        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['rating'] = res
        print(type(business))
        response_data['pos_rating'] = getNumPosRatings(business)
        response_data['neg_rating'] = getNumNegRatings(business)
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        #return HttpResponse("{'success':'true', 'rating': '" + str(rat) + "'}")
    else:
        raise Http404('What are you doing here?')


@csrf_exempt
def remove_tip_vote(request):
    log_msg('Remove Tip Vote!')
    if request.method == 'POST':
        try:
            tip = Tip.objects.get(id=request.POST['id'])
        except Tip.DoesNotExist:
            log_msg("Tip does not exist")
            return HttpResponse("{'success': 'false'}")

        try:
            rating = TipRating.objects.filter(tip=tip, user=request.user)
        except TipRating.DoesNotExist:
            print "Unexpected error:", sys.exc_info()[0]
            log_msg("Tip does not exist")
            print(tip.descr)
            pass
        else:
            log_msg("Deleting a tip rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(tip)
        response_data['neg_rating'] = getNumNegRatings(tip)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')


@csrf_exempt
def remove_tag_vote(request):
    log_msg('Remove Tag Vote!')
    if request.method == 'POST':
        try:
            tag = Tag.objects.get(id=request.POST['id'])
        except Tag.DoesNotExist:
            log_msg("Tag does not exist")
            return HttpResponse("{'success': 'false'}")

        try:
            rating = TagRating.objects.filter(tag=tag, user=request.user)
        except TagRating.DoesNotExist:
            print "Unexpected error:", sys.exc_info()[0]
            log_msg("Tag does not exist")
            print(tag.descr)
            pass
        else:
            log_msg("Deleting a tag rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(tag)
        response_data['neg_rating'] = getNumNegRatings(tag)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')


@csrf_exempt
def remove_review_vote(request):
    log_msg('Remove Review Vote!')
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=request.POST['id'])
        except Review.DoesNotExist:
            return HttpResponse("{'success': 'false'}")

        try:
            rating = ReviewRating.objects.filter(review=review, user=request.user)
        except ReviewRating.DoesNotExist:
            pass
        else:
            log_msg("Deleting a review rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(review)
        response_data['neg_rating'] = getNumNegRatings(review)

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
            log_msg("Deleting a rating")
            rating.delete()

        response_data = dict()
        response_data['id'] = str(request.POST['id'])
        response_data['success'] = 'true'
        response_data['pos_rating'] = getNumPosRatings(business)
        response_data['neg_rating'] = getNumNegRatings(business)

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        raise Http404('What are you doing here?')
