# Create your views here.
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from httplib import HTTPResponse
from ios_interface.utility import get_bus_data_ios
from ratings.models import Business
from ratings.utility import get_businesses_trending, get_bus_data, sort_trending
import json
import logging


logger = logging.getLogger(__name__)

def order_by_rating(b1,b2):
    
    if b1.rating and b2.rating:
        return cmp(b1.rating, b2.rating)
    elif b1.rating:
        return cmp(b1.rating, b2.recommendation)
    elif b2.rating:
        return cmp(b1.recommendation,b2.rating)
    else:
        return cmp(b1.recommendation, b2.recommendation)


def get_businesses(request):
    print(request.GET)
    uname = request.GET['uname']
    print('uname is ' + str(uname))
    try:
        user = User.objects.get(username=uname)
    except:
        logger.error("invalid useranme trying to get data")
    
    
    businesses = []
    try:
        businesses = Business.objects.all() # order by rating
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
    
        
    business_list = get_bus_data_ios(businesses,user)
    business_list = sorted(business_list,cmp=order_by_rating)
    data = serializers.serialize("xml", businesses)
    return HttpResponse(json.dumps(data), mimetype="application/json")

