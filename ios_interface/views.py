#from allsortz.search import get_all_nearby
from comments.models import Comment
from django.contrib.auth.models import User
from django.http import HttpResponse
from geopy import geocoders
from httplib import HTTPResponse
from ios_interface.authenticate import authenticate_api_request
from ios_interface.utility import get_bus_data_ios, get_single_bus_data_ios
from ratings.models import Business, Rating
from tags.models import BusinessTag
from tags.views import get_default_user
import json
import logging
import simplejson as json
from allsortz.search import get_all_nearby




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
    try:
        bus = Business.objects.get(id=oid)
    except: 
        return server_error('Business with id '+str(oid)+'not found')
        
        
    if 'rating' not in request.GET:
        return server_error('Rating not provided')
    
    rating = request.GET['rating']
    Rating.objects.create(business=bus, reating=rating,user=user) 
    bus_data = get_single_bus_data_ios(bus,user)
    return server_data(bus_data)
    
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


#    print('before neraby)')
    #nearby_businesses = get_all_nearby(lat,lng,3)
#    print('after nearby')

    MAX_RATING = 4.0
    DISTANCE = 3
    top_businesses = get_bus_data_ios(get_all_nearby(lat, lng, DISTANCE) ,user)

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


def get_business_categories(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
    return server_error("Unimplemented")

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
    
    #TODO serialize cateogry?
    return server_data(category)

def rate_business_category(request):
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
    return server_error("Unimplemented")


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
    return server_error("Unimplemented")

def rate_comment(request):
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
    
    if 'rating' not in request.GET:
        return server_error("No rating specified")
    
    return server_error("Unimplemented")



def get_photos(request):
    response_data = dict()
    response_data['success'] = False
    response_data['result'] = ''
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def get_photo(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    
    if 'type' not in request.GET:
        return server_error("Photo type not specified")
    
    oid = request.GET['id']
    phototype = request.GET['type']
    
#    if phototype=="business":
#        try:
#            photo = BusinessPhoto.objects.get(id=oid)
#        except: 
#            return server_error('BusinessPhoto with id '+str(oid)+'not found')
#    elif phototype=="user":
#            try:
#                photo = UserPhoto.objects.get(id=oid)
#            except: 
#                return server_error('UserPhoto with id '+str(oid)+'not found')
#    else:
#        return server_error("Invalid phototype specified: " + str(phototype))
#    
    return server_error("Unimplemented")

def rate_photo(request):
    try:
        user = authenticate_api_request(request)
    except:
        return server_error('Failure to authenticate')
        
    if 'id' not in request.GET:
        return server_error("No Comment ID provided")
    
    if 'type' not in request.GET:
        return server_error("Photo type not specified")
    
    if 'rating' not in request.GET:
        return server_error("Rating not specified for Photo")
    
    oid = request.GET['id']
    phototype = request.GET['type']
    rating = request.GET['rating']
#    
#    if phototype=="business":
#        try:
#            photo = BusinessPhoto.objects.get(id=oid)
#        except: 
#            return server_error('BusinessPhoto with id '+str(oid)+'not found')
#    elif phototype=="user":
#            try:
#                photo = UserPhoto.objects.get(id=oid)
#            except: 
#                return server_error('UserPhoto with id '+str(oid)+'not found')
#    else:
#        return server_error("Invalid phototype specified: " + str(phototype))


def get_queries(request):
    response_data = dict()
    response_data['success'] = False
    response_data['result'] = 'Not even the model is implemented yet'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def get_query(request):
    response_data = dict()
    response_data['success'] = False
    response_data['result'] = 'Not even the model is implemented yet'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

 
