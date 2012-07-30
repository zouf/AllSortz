'''
Created on Jul 26, 2012

@author: zouf
'''

from geopy import geocoders
from tags.views import get_default_user
def authenticate_api_request(request):
    user = get_default_user()
    g = geocoders.Google()
    _, (lat, lng) = g.geocode("Princeton, NJ") 
    user.current_location = (lat,lng) 
    return user