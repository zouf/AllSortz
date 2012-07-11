'''
Created on Jun 27, 2012

@author: zouf
'''
from communities.views import get_community, get_default
from django.contrib.auth.models import AnonymousUser
from ratings.favorite import is_user_subscribed
from ratings.models import Community, BusinessComment, CommentRating, TagComment, \
    Comment
from ratings.utility import get_lat, get_single_bus_data
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, HardTag, BusinessTag
from tags.views import get_tags_business, get_tags_user, get_top_tags, \
    get_hard_tags, get_all_sorts, get_master_summary_tag, get_pages, \
    get_bus_master_tag
import logging
from ratings.feed import get_bus_recent_activity


logger = logging.getLogger(__name__)


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


def get_tag_comments(b,tag):
    logger.debug('get for'+str(b)+ ' and tag ' + str(tag.descr))
    tagcomments = TagComment.objects.filter(business=b,tag=tag).order_by('-date')

    comment_list = []
    for tc in tagcomments:
        if tc.thread.reply_to is None: #root tag comment
            comment_list.append("open-even")
            recurse_comments(tc.thread,comment_list,False)
            comment_list.append("close")    
    results = []              
    for c in comment_list:
        if c != "open-even" and c != "open-odd" and c != "close":
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


def get_business_comments(business,user=False):
    buscomments = BusinessComment.objects.filter(business=business).order_by('-date')
    for bc in buscomments:
        print(bc.date)
    comment_list = []
    for bc in buscomments:
        if bc.thread.reply_to is None: #root tag comment
            comment_list.append("open-even")
            recurse_comments(bc.thread,comment_list,False)
            comment_list.append("close")    
    results = []              
    for c in comment_list:
        if c != "open-even" and c != "open-odd" and c != "close":
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

def get_default_tag_context(b,t,user):
    comments = get_tag_comments(b,t)
    bus_tags = get_tags_business(b,user=user,q="")

    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    hard_tags = get_hard_tags(b)
    
    pages = get_pages(b,bus_tags)
    b = get_single_bus_data(b,user)
    
    bus_master_tag = get_bus_master_tag(b,user=user,q="")
    master_page = get_pages(b,[bus_master_tag.tag])
        
    
    context =   { \
        'communities': Community.objects.all(),\
        'business' : b, \
        'comments': comments, \
        'lat': b.lat,\
        'lng':b.lon,  \
        'bus_tags':bus_tags, \
        'pages': pages, \
        'master_page':master_page,\
        'tags': Tag.objects.all(),\
        'user_sorts':user_tags,\
        'top_sorts':top_tags,\
        'all_sorts':get_all_sorts(4),\
        'hard_tags':hard_tags,\
        'location_term':get_community(user)
        }

    return context


def get_default_blank_context(user):
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    community = get_community(user)

    context = {\
               'communities': Community.objects.all(),\
              'community': community,\
              'user_sorts':user_tags,\
            'top_sorts':top_tags,\
             'tags': Tag.objects.all(),\
             'questions': HardTag.objects.all(),\
            'all_sorts':get_all_sorts(4),\
            'location_term':community }   
    return context     

def get_default_bus_context(b,user):
    comments = get_business_comments(b)
    bus_tags = get_tags_business(b,user=user,q="")
        
        
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    hard_tags = get_hard_tags(b)
    
    pages = get_pages(b,bus_tags)
    b = get_single_bus_data(b,user)
    context = {}
    context.update({
        'business' : b,
        'comments': comments, 
        'lat':b.lat,
        'lng':b.lon,  
        'bus_tags':bus_tags, 
        'pages': pages, 
        'master_summary': get_master_summary_tag(),
        'tags': Tag.objects.all().order_by('-descr').reverse(),
        'user_sorts':user_tags,
        'top_sorts':top_tags,
        'all_sorts':get_all_sorts(4),
        'hard_tags':hard_tags,
        'location_term':get_community(user) ,
        'communities': Community.objects.all(),
        'following_business': is_user_subscribed(b,user),
        'bus_activity_feed' : get_bus_recent_activity(b)
        })

    return context

def get_unauthenticated_context():
    top_tags = get_top_tags(10)
    context = { \
            'top_sorts':top_tags,\
            'all_sorts':get_all_sorts(4),\
            'location_term':get_community(None)\
            }
    return context
