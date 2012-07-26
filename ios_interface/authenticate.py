'''
Created on Jul 26, 2012

@author: zouf
'''
from tags.views import get_default_user
def authenticate_api_request(request):
    return get_default_user()