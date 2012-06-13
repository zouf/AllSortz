# Create your views here.
from comments.models import Comment, CommentRating
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ratings.models import Business
from recommendation.normalization import getNumPosRatings, getNumNegRatings
import logging
import sys

logger = logging.getLogger(__name__)

#sorts comments
def comment_comp(x,y):
    #eventually do something more intelligent here!
    xTot = x.pos_ratings - x.neg_ratings
    yTot = y.pos_ratings - y.neg_ratings
    if (xTot > yTot):
        return -1
    elif (xTot < yTot ):
        return 1
    else:
        return 0


#adds comments to the database
@csrf_exempt
def add_comment(request):
    logger.debug('in add comment')
    if request.method == 'POST':  # add a comment!
        form = request.POST       
        #base comment submission
        if 'cid' not in form:      
            nm = form['comment']
            bid = form['bid']
            b = Business.objects.get(id=bid)
            keyset = Comment.objects.filter(descr=nm, business=b)
            if(keyset.count() == 0):
                try:
                    k = Comment.objects.create(descr=nm,user=request.user,business=b,reply_to=None)
                except:
                    logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                k.save()
        else:  #reply to another comment submission
            nm = form['comment']
            bid = form['bid']
            b = Business.objects.get(id=bid)
            cid = form['cid']
            c = Comment.objects.get(id=cid)
            keyset = Comment.objects.filter(descr=nm, business=b)
            if(keyset.count() == 0):
                try:
                    k = Comment.objects.create(descr=nm,user=request.user,business=b,reply_to=c)
                except:
                    logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                k.save()
        comment_list = get_comments(b)
        return render_to_response('comments/thread.html', {'business':b, 'comments': comment_list})



def recurse_comments(comment,cur_list):
    cur_list.append(comment)
    replies = Comment.objects.filter(reply_to=comment)
    for c in replies:
        cur_list.append("open")
        recurse_comments(c,cur_list)
        cur_list.append("close")

#gets all the comments, including nested ones
#adds tokens "open" and "close" to denote subcomments
def get_comments(b,user=False,q=""):
    if q != "":
        comments = Comment.objects.filter(descr__icontains=q)[:20]
    else:
        comments = Comment.objects.filter(business=b)
    
  
    comment_list = []
    for c in comments:
        if c.reply_to is None:
            comment_list.append("open")
            recurse_comments(c,comment_list)
            comment_list.append("close")
    
    results = []              
    for c in comment_list:
        if c != "open" and c != "close":
            try:
                rat =  CommentRating.objects.get(comment=c)
                c.this_rat = rat.rating
                c.pos_ratings = getNumPosRatings(c)
                c.neg_ratings = getNumNegRatings(c)
            except:
                c.this_rat = 0
                c.pos_ratings = 0
                c.neg_ratings = 0
        results.append(c)
    return results