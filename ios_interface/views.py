#from allsortz.search import get_all_nearby
from allsortz.search import get_all_nearby
from comments.models import Comment
from django.http import HttpResponse
from geopy import geocoders
from ios_interface.authenticate import authenticate_api_request
from ios_interface.models import Photo, PhotoRating
from ios_interface.serializer import get_category_data, get_categories_data, \
    get_comment_data, get_photo_data, get_photos_data, get_query_data, \
    get_queries_data
from ios_interface.utility import get_bus_data_ios, get_single_bus_data_ios
from queries.models import Query
from ratings.models import Business, Rating, CommentRating
from tags.models import BusinessTag, TagRating, Tag
from tags.views import get_default_user
import logging
import simplejson as json
from ratings.utility import setBusLatLng

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
    except:
        return server_error('Failure to authenticate')
    
    if 'id' not in request.GET:
        return server_error('ID not provided')
    
    oid = request.GET['id']
    try:
        bus = Business.objects.get(id=oid)
    except: 
        return server_error('Business with id '+str(oid)+'not found')

    bus.dist = 6.66
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)

def rate_business(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
    
    if 'id' not in request.GET:
        return server_error('ID not provided')
    oid = request.GET['id']

    if 'rating' not in request.GET:
        return server_error('Rating not provided')
    rating = request.GET['rating']
    
    try:
        bus = Business.objects.get(id=oid)
    except: 
        return server_error('Business with id '+str(oid)+'not found')    
        
    if Rating.objects.filter(business=bus,user=user).count() > 0:
        Rating.objects.filter(business=bus,user=user).delete()
    Rating.objects.create(business=bus, rating=rating,user=user) 
    bus.dist = 6.66
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)
    
def add_business(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
    
    if 'businessName' not in request.GET:
        return server_error("Name not provided")
    businessName = request.get['businessName']
    
    if 'streetAddr' not in request.GET:
        return server_error("Address not provided")
    streetAddr = request.get['streetAddr']
    
    if 'businessCity' not in request.GET:
        return server_error("City not provided")
    businessCity = request.GET['businessCity']

    if 'businessPhone' not in request.GET:
        return server_error("Phone not provided")
    businessPhone = request.GET['businessPhone']
    
    if 'businessState' not in request.GET:
        return server_error("state not provided")
    businessState = request.GET['businessState']
    
    if Business.objects.filter(name=businessName,addr=streetAddr, city=businessCity, state=businessState).count() > 0:
        return server_error("Business already exists")
    else:
        bus= Business.objects.create(name=businessName,city=businessCity,state=businessState)
    
    bus.dist = 6.66
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)

def modify_business(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
    
    if 'id' not in request.GET:
        return server_error("ID not provided for business")
    oid = request.GET['id']
    
    try:
        bus = Business.objects.get(id = oid)
    except:
        return server_error("Getting business with id "+str(oid)+" failed")
    
    if 'businessName' in request.GET:
        bus.name = request.GET['businessName']
    
    if 'streetAddr'  in request.GET:
        bus.addr = request.get['streetAddr']
    
    if 'businessCity'  in request.GET:
        bus.city = request.get['businessCity']

    if 'businessPhone'  in request.GET:
        return server_error("Phone not implemented")
    
    if 'businessState' in request.GET:
        bus.state = request.GET['businessState']
        
    bus.save()
    bus.dist = 6.66
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)

def remove_business(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
    
    if 'id' not in request.GET:
        return server_error("ID not provided for business")
    oid = request.GET['id']
    
    try:
        bus = Business.objects.get(id=oid)
        name = bus.name
        Business.objects.filter(id = oid).delete()
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
        place, (lat, lng) = g.geocode("Princeton, NJ")  


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
    except:
        return server_error('Failure to authenticate')
    if 'id' not in request.GET:
        return server_error("No Business ID provided")
    oid = request.GET['id']
    
    try:
        bus = Business.objects.get(id=oid)
    except: 
        return server_error('Business with id '+str(oid)+'not found')
        
    categories = BusinessTag.objects.filter(business=bus)
    
    data = get_categories_data(categories,user)
    return server_data(data)

def get_business_category(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Category ID provided")
    oid = request.GET['id']
    
    try:
        category = BusinessTag.objects.get(id=oid)
    except: 
        return server_error('Category with id '+str(oid)+'not found')
    
    data = get_category_data(category,user)
    return server_data(data)

def rate_business_category(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Category ID provided")
    oid = request.GET['id']
    
    if 'rating' not in request.GET:
        return server_error('Rating not provided')
    rating = request.GET['rating']
   
    try:
        category = BusinessTag.objects.get(id=oid)
    except: 
        return server_error('Category with id '+str(oid)+'not found')
    
    TagRating.objects.create(user=user,tag=category,rating=rating)
    
    data = get_category_data(category,user)
    return server_data(data)

def add_business_cateogry(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
    if 'id' not in request.GET:
        return server_error("No BUsiness ID provided")
    oid = request.GET['id']
    
    if 'tagid' not in request.GET:
        return server_error("No Category ID provided")
    tagid = request.GET['tagid']
    
    try:
        bus = Business.objects.get(id=oid)
        tag = Tag.objects.get(id=tagid)
    except: 
        return server_error('Retrieving business and category failed (IDs: '+str(oid)+ ' and ' + str(tagid))
    
    if BusinessTag.objects.filter(business=bus,tag=tag).count() > 0:
        category = BusinessTag.objects.get(business=bus, tag=tag)
    else:
        category = BusinessTag.objects.create(business=bus,tag=tag,creator=user)
    data = get_category_data(category,user)
    return server_data(data)

def remove_business_cateogry(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Category ID provided")
    oid = request.GET['id']
    
    try:
        category = BusinessTag.objects.filter(id=oid).delete()
    except: 
        return server_error('Category with id '+str(oid)+'not found')
    
    data = get_category_data(category,user)
    return server_data(data)

'''
Code to handle comments
'''


def get_comment(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    
    oid = request.GET['id']
    try:
        comment = Comment.objects.get(id=oid)
    except: 
        return server_error('Comment with id '+str(oid)+'not found')
    
    data = get_comment_data(comment,user)
    return server_data(data)

def rate_comment(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    oid = request.GET['id']

    if 'rating' not in request.GET:
        return server_error("No rating specified")
    rating = request.GET['rating']
    
    try:
        comment = Comment.objects.get(id=oid)
    except: 
        return server_error('Comment with id '+str(oid)+'not found')

    CommentRating.objects.create(user=user,rating=rating,comment=comment)
    data = get_comment_data(comment,user)
    return server_data(data)

def add_comment(request):
    return server_error("unimplemented")

def remove_comment(request):
    return server_error("unimplemented")


'''
Code to handle photos
'''

def get_photos(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    oid = request.GET['id']
        
    if 'type' not in request.GET:
        return server_error("Photo type not specified")
    phototype = request.GET['type']
    
    if 'order_by' not in request.GET:
        return server_error("Order by not specified: date, rating are options")
    order_by = request.GET['order_by']
        
    
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
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    oid = request.GET['id'] 
    
    try:
        photo = Photo.objects.get(id=oid)
    except: 
        return server_error('Photo with id '+str(oid)+'not found')
    
    data = get_photo_data(photo,user)
    return server_data(data)

def rate_photo(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    oid = request.GET['id']
    
    if 'rating' not in request.GET:
        return server_error("Rating not specified for Photo")
    rating = request.GET['rating']

    photo = Photo.objects.get(id=oid)            
    PhotoRating.objects.create(rating = rating,user=user,photo=photo)
    data = get_photo_data(photo,user)
    return server_data(data)
    
 
def add_photo(requst):
    return server_error("unimplemented")

def remove_photo(requst):
    return server_error("unimplemented")


'''
Code to handle queries
''' 

def get_queries(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
            
    if 'type' not in request.GET:
        return server_error("No Query Type provided")
    querytype = request.GET['type']
    
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
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    oid = request.GET['id']
    
    try:
        query = Query.objects.get(id=oid)
    except:
        return server_error("Query with ID "+str(oid)+" not found")

    data = get_query_data(query,user)
    return server_data(data)
 
def add_query(requst):
    return server_error("unimplemented")

def remove_query(requst):
    return server_error("unimplemented")
 
def modify_query(requst):
    return server_error("unimplemented")
 
 
def prepop_queries(user):
    user = get_default_user()
    for t in Tag.objects.all():
        q = Query(name=t.descr,proximity=5,value=5,score=5,price=5,visited=False,deal=False,networked=False,text="",creator=user,is_default=True)
        q.save()
        
        
