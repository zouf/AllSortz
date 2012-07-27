from allsortz.views import get_tag_comments, get_business_comments
from comments.models import Comment, TagComment, BusinessComment, PhotoComment
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from photos.models import BusinessPhoto
from photos.views import get_photo_comments
from ratings.models import Business, CommentRating
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag
import json
import logging
import sys
#from photos.models import BusinessPhoto
#from photos.views import get_photo_comments


logger = logging.getLogger(__name__)
@csrf_exempt
def add_tag_comment(request):
    logger.debug('in add comment')
    if request.method == 'POST':  # add a comment!
        form = request.POST 
        #add a comment to a business' tag page 
        if 'tid'  in form:
            bid =form['bid']
            b = Business.objects.get(id=bid)
            tid = form['tid']
            t = Tag.objects.get(id=tid)
            if 'cid' not in form:  #root reply
                nm = form['comment']
                k = Comment(descr=nm,user=request.user,reply_to=None)
                k.save()
                tc = TagComment(business=b,tag=t,thread=k)
                tc.save()
            else:  #reply to another comment submission
                nm = form['comment']
                cid = form['cid']
                parent = Comment.objects.get(id=cid) #parent comment
                k = Comment.objects.create(descr=nm,user=request.user,reply_to=parent) #new child
                k.save()
            comment_list = get_tag_comments(b,t)
            return render_to_response('ratings/discussion/thread.html', {'tag':t, 'business': b, 'comments': comment_list})
        
        # add a comment to a business's page alone
        else:
            bid =form['bid']
            b = Business.objects.get(id=bid)
            if 'cid' not in form:      #root reply
                nm = form['comment']
                k = Comment(descr=nm,user=request.user,reply_to=None)
                k.save()
                bc = BusinessComment(business=b,thread=k)
                bc.save()
            else:  #reply to another comment submission
                nm = form['comment']
                cid = form['cid']
                parent = Comment.objects.get(id=cid) #parent comment
                k = Comment.objects.create(descr=nm,user=request.user,reply_to=parent)
                k.save()
            comment_list = get_business_comments(b)
            return render_to_response('ratings/discussion/thread.html', {'business':b, 'comments': comment_list})

def recurse_comments(comment,cur_list,even):
    cur_list.append(comment)
    replies = Comment.objects.filter(reply_to=comment).order_by('-date')
    for c in replies:
        if even:
            cur_list.append("open-even")
        else:
            cur_list.append("open-odd")
        recurse_comments(c,cur_list,not even)
        cur_list.append("close")


def add_photo_comment(request):
    logger.debug(' adding a photo comment')
    if request.method == 'POST':  # add a comment!
        form = request.POST 
        if 'pid' not in form:
            logger.error('no photo id for add photo comment')
        phid = form['pid']
        photo = BusinessPhoto.objects.get(id=phid)
        if 'cid' not in form:      #root
            nm = form['comment']
            k = Comment(descr=nm,user=request.user,reply_to=None)
            k.save()
            pc = PhotoComment(photo=photo,thread=k)
            pc.save()
        else:
            nm = form['comment']
            cid = form['cid']
            parent = Comment.objects.get(id=cid) #parent comment
            k = Comment.objects.create(descr=nm,user=request.user,reply_to=parent)
            k.save()
        comment_list = get_photo_comments(photo)
        return render_to_response('ratings/discussion/thread.html', {'p':photo, 'comments': comment_list})
            

@csrf_exempt
def comment_vote(request):

    logger.debug('in comment_vote')
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=(request.POST['id']))
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
            comment = Comment.objects.get(id=(request.POST['id']))
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

