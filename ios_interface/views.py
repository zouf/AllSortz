from django.contrib.auth.models import User
from django.http import HttpResponse
from httplib import HTTPResponse
from ios_interface.utility import get_bus_data_ios
from ratings.models import Business
from ratings.utility import get_businesses_trending, get_bus_data, sort_trending
import json
import logging
import simplejson as json


logger = logging.getLogger(__name__)

def order_by_rating(b1,b2):
    print(b1)
    if b1['rating'] and b2['rating']:
        return cmp(b1['rating'], b2['rating'])
    elif b1['rating']:
        return cmp(b1['rating'], b2['recommendation'])
    elif b2['rating']:
        return cmp(b1['recommendation'],b2['rating'])
    else:     
        return cmp(b1['recommendation'], b2['recommendation'])


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
    
    #distance weight
    if 'dw' in request.GET:
        dw = request.GET['dw']
        
    #price weight
    if 'pw' in request.GET:
        pw = request.GET['pw']
        
    #value weight
    if 'vw' in request.GET:
        vw = request.GET['vw']

    #Tags to sort by
    if 'tags' in request.GET:  
        tags = request.get['tags']

    
    businesses = []
    try:
        businesses = Business.objects.all() # order by rating
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
    
        
    business_list = get_bus_data_ios(businesses,user)
    business_list = sorted(business_list,cmp=order_by_rating)

    response_data = dict()
    response_data['success'] = True
    response_data['result'] = business_list
    return HttpResponse(json.dumps(response_data), mimetype="application/json")



