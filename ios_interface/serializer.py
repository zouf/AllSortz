'''
Created on Jul 27, 2012

@author: zouf
'''
from comments.models import Comment
from ios_interface.models import PhotoRating
from queries.models import QueryTag
from ratings.models import CommentRating, PageRelationship
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import UserTag
from wiki.models import Page
import logging

logger = logging.getLogger(__name__)

def get_category_data(category,user):
    data = dict()
    data['categoryName'] = category.tag.descr
    data['categoryID'] = category.id
    numPositive = getNumPosRatings(category)
    numNegative = getNumNegRatings(category)
    totalRatings = numPositive+numNegative
    if totalRatings != 0:
        data['categoryRating'] = numPositive / totalRatings
    else:
        data['categoryRating'] = 0.0

    try:
        pgr = PageRelationship.objects.get(businesstag=category)
    except PageRelationship.DoesNotExist:
        pg = Page.objects.create(name=category.tag.descr)
        pgr = PageRelationship.objects.create(businesstag=category,page = pg)
        
    
    data['categoryContent'] = pgr.page.rendered
    tagfilter = UserTag.objects.filter(user=user,tag=category)
    if tagfilter.count() > 0:
        data['userIsSubscribed'] = True
    else:
        data['userIsSubscribed'] = False 
    return data

def get_categories_data(categories,user):
    data = []
    for cat in categories:
        data.append(get_category_data(cat,user))
    return data
    

def get_comment_data(comment,user):
    data = dict()
    data['commentCreator'] = comment.user.username
    data['posted'] = comment.date
    data['content'] = comment.descr
    numPositive = getNumPosRatings(comment)
    numNegative = getNumNegRatings(comment)
    data['positiveVotes'] = numPositive
    data['negativeVotes'] = numNegative
    
    try:
        thisUsersRating = CommentRating.objects.get(comment=comment,user=user)
    except:
        thisUsersRating = None
    
    data['thisUsersRating'] = thisUsersRating       
    return data
    
    
def get_comments_data(comments,user):
    data = []
    for c in comments:
        data.append(get_comment_data(c,user))
    return data


def get_photo_data(photo,user):
    data = dict()
    data['photoTitle'] = photo.title
    data['photoCaption'] = photo.caption
    data['photoURL'] = photo.image.url
    data['photoCreator'] = photo.user.username
    numPositive = getNumPosRatings(photo)
    numNegative = getNumNegRatings(photo)
    data['positiveVotes'] = numPositive
    data['negativeVotes'] = numNegative
    
    try:
        thisUsersRating = PhotoRating.objects.get(photo=photo,user=user)
    except:
        thisUsersRating = None
    
    data['thisUsersRating'] = thisUsersRating       
    return data

def get_photos_data(photos,user,order_by):
    data = []
    for p in photos:
        data.append(get_photo_data(p,user))
    
    if order_by == 'date':
        print('order by date')
    else:
        print('order by rating')
    return data

def get_query_data(query,user):
    data=dict()
    data['queryName'] = query.name
    data['queryCreator'] = query.creator.username
    data['proximityWeight'] = query.proximity
    data['priceWeight'] = query.price
    data['valueWeight'] = query.value
    data['scoreWEight'] = query.score
    
    data['userHasVisited'] = query.visited
    
    data['searchText'] = query.text

    data['networked'] = query.networked
    data['deal'] = query.deal
    data['visited'] = query.visited
    
    data['isCreatedByUs'] = query.is_default
    
    queryTags = []
    for qt in QueryTag.objects.filter(query=query):
        queryTags.append(get_category_data(qt.tag,user))
    data['queryCategories'] = queryTags
    
    return data

def get_queries_data(queries,user):
    data = []
    for q in queries:
        data.append(get_query_data(q,user))
    return data
    