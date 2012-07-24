from allsortz.search import get_all_nearby
from django.contrib.auth.models import User
from django.http import HttpResponse
from geopy import geocoders
from httplib import HTTPResponse
from ios_interface.utility import get_bus_data_ios
from ratings.models import Business
import json
import logging
import simplejson as json


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


# < 0 => b1 > b2
# 0 => b1 equiv b2
# > 0 => b


def get_businesses(request):

    
    if 'uname' not in request.GET:
        response_data = dict()
        logger.error('invalid query to server. No username')
        response_data['success'] = False
        response_data['result'] = ' no username given'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

        
    #username
    uname = request.GET['uname'] 
    try:
        user = User.objects.get(username=uname)
    except:
        response_data = dict()
        logger.error("invalid username trying to get data")
        response_data['success'] = False
        response_data['result'] = 'Invalid username'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    
    
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


    print('before neraby)')
    #nearby_businesses = get_all_nearby(lat,lng,3)
    print('after nearby')

    MAX_RATING = 4.0
    DISTANCE = 3
    
    
    

    top_businesses = get_bus_data_ios(get_all_nearby(lat, lng, DISTANCE) ,user)

    #NORMALIZATION
    for b in top_businesses:
        if 'rating' in b:
            #print('rating at '+str(b['rating']))
            b['weight'] = sw*(float(b['rating'])/MAX_RATING) 
        
        else:
            #print('rec at ' + str(b['recommendation']))       
            b['weight'] = sw*float((b['recommendation'])/MAX_RATING)
        b['weight'] +=  dw*((DISTANCE - float(b['dist'])/DISTANCE))
        #print('weight is ' + str(b['weight']))
    top_businesses = sorted(top_businesses,cmp=order_by_weight)
    
    response_data = dict()
    response_data['success'] = True
    response_data['result'] = top_businesses
    return HttpResponse(json.dumps(response_data), mimetype="application/json")



