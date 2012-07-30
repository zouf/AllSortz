#from allsortz.search import get_all_nearby
from allsortz.search import get_all_nearby
from comments.models import Comment
from django.http import HttpResponse
from geopy import geocoders, distance
from ios_interface.authenticate import authenticate_api_request, \
    AuthenticationFailed
from ios_interface.models import Photo, PhotoRating, BusinessDiscussion, \
    CategoryDiscussion, PhotoDiscussion
from ios_interface.photos import add_photo_by_upload, add_photo_by_url
from ios_interface.serializer import get_category_data, get_categories_data, \
    get_comment_data, get_photo_data, get_photos_data, get_query_data, \
    get_queries_data
from ios_interface.utility import get_bus_data_ios, get_single_bus_data_ios, \
    ReadJSONError, get_json_post_or_error, get_json_get_or_error
from queries.models import Query, QueryTag
from ratings.models import Business, Rating, CommentRating
from ratings.utility import setBusLatLng
from tags.models import BusinessTag, TagRating, Tag
from tags.views import get_default_user
import logging
import simplejson as json

MAX_RATING = 4.0
DISTANCE = 3


logger = logging.getLogger(__name__)

def order_by_rating(b1,b2):

    if b1['rating'] and b2['rating']:
        return cmp(b1['rating'], b2['rating'])
    elif b1['rating']:
        return cmp(b1['rating'], b2['recommendation'])
    elif b2['rating']:
        return cmp(b1['recommendation'],b2['rating'])
    else:     
        return cmp(b1['recommendation'], b2['recommendation'])
    
def order_by_weight(b1,b2):

    if b1['weight'] and b2['weight']:
        return cmp(b2['weight'], b1['weight'])
    elif b1['weight']:
        return cmp(b2['weight'], b1['weight'])
    elif b2['weight']:
        return cmp(b2['weight'],b1['weight'])
    else:     
        return cmp(b2['weight'], b1['weight'])
    
def get_user(request):
    return get_default_user()

def server_error(msg):
    response_data = dict()
    response_data['success'] = False
    response_data['result'] = msg
    return HttpResponse(json.dumps(response_data), mimetype="application/json")    

def server_data(data):
    response_data = dict()
    response_data['success'] = True
    response_data['result'] = data
    return HttpResponse(json.dumps(response_data), mimetype="application/json")    

'''
Code to handle businesses
'''

def get_business(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        bus = Business.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Business with id '+str(oid)+'not found')

    bus.dist = distance.distance(user.current_location,(bus.lat,bus.lon)).miles
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)

def rate_business(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        rating = get_json_get_or_error('rating', request)
        bus = Business.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Business with id '+str(oid)+'not found')    
        
    if Rating.objects.filter(business=bus,user=user).count() > 0:
        Rating.objects.filter(business=bus,user=user).delete()
    Rating.objects.create(business=bus, rating=rating,user=user) 
    bus.dist = distance.distance(user.current_location,(bus.lat,bus.lon)).miles
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)
    
def add_business(request):
    try:
        user = authenticate_api_request(request)
        bus = Business()
        name=get_json_post_or_error('businessName', request)
        addr=get_json_post_or_error('streetAddr', request)
        city = get_json_post_or_error('businessCity', request)
        state = get_json_post_or_error('businessState', request)
        phone =  get_json_post_or_error('businessPhone', request)
        
        #already exists
        if Business.objects.filter(name=name,addr=addr,city=city,state=state).count() ==  0:
            bus = Business.objects.create(name=name,addr=addr,city=city,state=state)
        elif Business.objects.filter(name=name,addr=addr,city=city,state=state).count() > 1: #too many
            Business.objects.filter(name=name,addr=addr,city=city,state=state).delete()
            bus = Business.objects.create(name=name,addr=addr,city=city,state=state)
        else:
            bus = Business.objects.get(name=name,addr=addr,city=city,state=state)                    
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value) 
    bus.dist = distance.distance(user.current_location,(bus.lat,bus.lon)).miles
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)

def edit_business(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        bus = Business.objects.get(id = oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)   
    except:
        return server_error("Getting business with id "+str(oid)+" failed")
    
    print(request.POST)
    if 'businessName' in request.POST:
        print('mod that stuff!')
        bus.name = request.POST['businessName']
    
    if 'streetAddr'  in request.POST:
        bus.addr = request.POST['streetAddr']
    
    if 'businessCity'  in request.POST:
        bus.city = request.POST['businessCity']

    if 'businessPhone'  in request.POST:
        return server_error("Phone not implemented")
    
    if 'businessState' in request.POST:
        bus.state = request.POST['businessState']
        
    print(bus.name)
    bus.save()
    print(bus.name)
    bus.dist = distance.distance(user.current_location,(bus.lat,bus.lon)).miles
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)

def remove_business(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        bus = Business.objects.get(id=oid)
        name = bus.name
        Business.objects.filter(id = oid).delete()
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except:
        return server_error("Deleting business with id "+str(oid)+" failed")
    return server_data("Deletion of business "+str(name)+ " was a success")

def get_businesses(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    #Weights for sorting. 
    #score weight
    if 'sw' in request.GET:
        sw = request.GET['sw']
    else:
        sw = 1
    
    #distance weight
    if 'dw' in request.GET:
        dw = request.GET['dw']
    else:
        dw = 1
        
    #price weight
    if 'pw' in request.GET:
        pw = request.GET['pw']
    else:
        pw = 1
        
    #value weight
    if 'vw' in request.GET:
        vw = request.GET['vw']
    else:
        vw = 1

    #Tags to sort by
    if 'tags' in request.GET:  
        tags = request.get['tags']


    if 'lat' in request.GET and 'lng' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']
    else:
        g = geocoders.Google()
        _, (lat, lng) = g.geocode("Princeton, NJ")  


    nearby_businesses = get_all_nearby(lat,lng,DISTANCE)
    top_businesses = get_bus_data_ios(nearby_businesses ,user)
    
    #NORMALIZATION
    for b in top_businesses:
        if 'ratingForCurrentUser' != 0:
            #print('rating at '+str(b['rating']))
            b['weight'] = sw*(float(b['ratingForCurrentUser'])/MAX_RATING) 
        
        else:
            #print('rec at ' + str(b['recommendation']))       
            b['weight'] = sw*float((b['ratingRecommendation'])/MAX_RATING)
        b['weight'] +=  dw*((DISTANCE - float(b['distanceFromCurrentUser'])/DISTANCE))
        #print('weight is ' + str(b['weight']))
    top_businesses = sorted(top_businesses,cmp=order_by_weight)
    return server_data(top_businesses)


'''
Code to handle business categories
'''


def get_business_categories(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        bus = Business.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Business with id '+str(oid)+'not found')
        
    categories = BusinessTag.objects.filter(business=bus)
    
    data = get_categories_data(categories,user)
    return server_data(data)

def get_business_category(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        category = BusinessTag.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Category with id '+str(oid)+'not found')
    
    data = get_category_data(category,user)
    return server_data(data)

def rate_business_category(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        rating = get_json_get_or_error('rating', request)
        category = BusinessTag.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Category with id '+str(oid)+'not found')
    
    TagRating.objects.create(user=user,tag=category,rating=rating)
    
    data = get_category_data(category,user)
    return server_data(data)

def add_business_category(request):
    try:
        user = authenticate_api_request(request)
        tagid = get_json_get_or_error('tagID', request)
        oid = get_json_get_or_error('businessID', request)
        bus = Business.objects.get(id=oid)
        tag = Tag.objects.get(id=tagid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Retrieving business and category failed (IDs: '+str(oid)+ ' and ' + str(tagid))
    
    if BusinessTag.objects.filter(business=bus,tag=tag).count() > 0:
        category = BusinessTag.objects.get(business=bus, tag=tag)
    else:
        category = BusinessTag.objects.create(business=bus,tag=tag,creator=user)
    data = get_category_data(category,user)
    return server_data(data)

def remove_business_category(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        BusinessTag.objects.filter(id=oid).delete()
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except:
        return server_error('Category with id '+str(oid)+'not found')
    return server_data("Deletion successful")

'''
Code to handle comments
'''


def get_comment(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        comment = Comment.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    
    data = get_comment_data(comment,user)
    return server_data(data)

def rate_comment(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        rating = get_json_get_or_error('rating', request)
        comment = Comment.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except: 
        return server_error('Comment with id '+str(oid)+'not found')

    CommentRating.objects.create(user=user,rating=rating,comment=comment)
    data = get_comment_data(comment,user)
    return server_data(data)

def add_comment(request):
    try: 
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('commentBaseID', request)  
        commentType = get_json_get_or_error('type', request)  
        content = get_json_post_or_error('commentContent', request)  
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)

    try:
        if 'replyToID' in request.POST:
            replyToID = request.GET['replyTo']
            replyComment = Comment.objects.get(id=replyToID)
        else:
            replyComment = None
    except:
        return server_error("No comment found with id "+str(replyToID))
    
    if commentType == 'business':
        try:
            bus = Business.objects.get(id=oid)
        except:
            return server_error("Business with ID "+str(oid)+ " does not exist")
        comment = BusinessDiscussion.objects.create(user=user,reply_to=replyComment,content=content,business=bus)
    elif commentType == 'category':
        try:
            btag = BusinessTag.objects.get(id=oid)
        except:
            return server_error("Category with ID "+str(oid)+ " does not exist")
        comment = CategoryDiscussion.objects.create(user=user,reply_to=replyComment,content=content,businesstag=btag)
    elif commentType == 'photo':
        try:
            photo = Photo.objects.get(id=oid)
        except:
            return server_error("Photo with ID "+str(oid)+ " does not exist")
        comment = PhotoDiscussion.objects.create(user=user,reply_to=replyComment,content=content,photo=photo)  
    else:
        return server_error("Invalid commentType "+str(commentType))
    data = get_comment_data(comment,user)
    return server_data(data)

def edit_comment(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)  
        content = get_json_post_or_error('commentContent', request)  
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    
    comment = CategoryDiscussion.objects.create(id=oid,content=content)
    data = get_comment_data(comment,user)
    return server_data(data)
    
def remove_comment(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)  
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    
    try:
        Comment.objects.filter(id=oid).delete()
    except: 
        return server_error('Comment with id '+str(oid)+' not found. Deletion failed')
    
    return server_data("Deletion successful")


'''
Code to handle photos
'''

def get_photos(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)  
        phototype = get_json_get_or_error('type', request)  
        order_by = get_json_get_or_error('order_by', request)  
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)

    
    if phototype=="business":
        try:
            bus = Business.objects.get(id=oid)
        except:
            return server_error("No business with ID"+str(oid)+" found")
        allphotos= Photo.objects.filter(business=bus)           
    else:
        allphotos= Photo.objects.filter(user=user,business=None)
        
    data = get_photos_data(allphotos,user,order_by=order_by)
    return server_data(data)


def get_photo(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        photo = Photo.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)       
    except Photo.DoesNotExist: 
        return server_error('Photo with id '+str(oid)+' not found. Deletion failed')
    
    data = get_photo_data(photo,user)
    return server_data(data)

def rate_photo(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        rating = get_json_get_or_error('rating', request)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)


    photo = Photo.objects.get(id=oid)            
    PhotoRating.objects.create(rating = rating,user=user,photo=photo)
    data = get_photo_data(photo,user)
    return server_data(data)
    
 
def add_photo(request):
    try:
        user = authenticate_api_request(request)
        caption = get_json_post_or_error('photoCaption', request)
        title = get_json_post_or_error('photoTitle', request)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
        
    if 'businessID' not in request.GET:
        b = None
        defaultUserPhoto = True

    else:
        defaultUserPhoto = False

        bid = request.GET['businessID']
        try:
            b = Business.objects.get(id=bid)
        except:
            return server_error("Could not retrieve business with ID "+str(bid)+ " for add_photo")

    
    if 'image' in request.FILES:
        img = request.FILES['image']
        photo = add_photo_by_upload(img,b,request.user,defaultUserPhoto,caption,title)
    elif 'url' in request.POST:
        url = request.POST['url']
        if url != '':
            photo = add_photo_by_url(url, b, request.user, defaultUserPhoto,caption,title)
    else:
        return server_error("No photo specified in request.FILES or URL in request.POST")
    data = get_photo_data(photo,user)
    return server_data(data)

def remove_photo(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        Photo.objects.filter(id=oid).delete()
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)      
    except Photo.DoesNotExist: 
        return server_error('Photo with id '+str(oid)+' not found. Deletion failed')
    return server_data("Deletion of photo id= " +str(oid)+ " successful")


'''
Code to handle queries
''' 

def get_queries(request):
    try:
        user = authenticate_api_request(request)
        querytype = get_json_get_or_error('type', request)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
      
    if querytype=='yours':
        queries = Query.objects.filter(creator=user)
    elif querytype=='popular': 
        queries = Query.objects.filter(is_default=True)
    else:
        queries = Query.objects.filter(creator=user)
    data = get_queries_data(queries,user)
    return server_data(data)
    
    
def get_query(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        query = Query.objects.get(id=oid)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except:
        return server_error("Query with ID "+str(oid)+" not found")

    data = get_query_data(query,user)
    return server_data(data)
 

    
def add_query(request):
    try:
        user = authenticate_api_request(request)
        query = Query()
        query.name = get_json_post_or_error('queryName',request)
        query.creator = user#get_json_or_error('queryName',request)
        query.proximity = get_json_post_or_error('proximityWeight',request)
        query.price = get_json_post_or_error('priceWeight',request)
        query.value = get_json_post_or_error('valueWeight',request)
        query.score = get_json_post_or_error('scoreWeight',request)
        query.userHasVisited = get_json_post_or_error('userHasVisited',request)
        query.text = get_json_post_or_error('searchText',request)
        query.networked = get_json_post_or_error('networked',request)
        query.deal = get_json_post_or_error('deal',request)
        query.is_default = False# get_json_or_error('deal',request)
        query.save()
        if 'queryCategories' not in request.POST:
            return server_error("Key queryCategories did not provide a list")
        categoryList = request.POST.getlist('queryCategories')
        for c in categoryList:
            if Tag.objects.filter(id=c).count() == 0:
                return server_error("Invalid Category provided")
            cat = Tag.objects.get(id=c)
            QueryTag.objects.create(query=query,tag=cat)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except:
        return server_error("Could not save the object")
    data = get_query_data(query,user)
    return server_data(data)

def remove_query(request):
    try:
        user = authenticate_api_request(request)
        oid = get_json_get_or_error('id', request)
        Query.objects.filter(id=oid).delete(0)
    except ReadJSONError as e:
        return server_error(e.value)
    except AuthenticationFailed as e:
        return server_error(e.value)
    except:
        return server_error("Query with ID "+str(oid)+" not found. Deletion was not successful")
    return server_data("Deletion successful")

 
def edit_query(requst):
    return server_error("unimplemented")
 

        
        
