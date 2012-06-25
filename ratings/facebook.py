'''
Created on Jun 25, 2012

@author: zouf
'''
from IPython.config.configurable import MultipleInstanceError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rateout.settings import FB_APP_SECRET, FB_APP_ID
from ratings.models import FacebookUser
from ratings.views import index
import base64
import cgi
import hashlib
import hmac
import json
import logging
import urllib


logger = logging.getLogger(__name__)

def handle_fb_login(request):
    if request.method == 'POST':
        response = request.POST['response']
        sig = response['authResponse']['signedRequest']
        fbuid = response['authResponse']['userID']
        try:
            fbu = FacebookUser.objects.get(fbuser_id=fbuid)
        except(MultipleInstanceError):
            fbu = FacebookUser.objects.filter(fbuser_id=fbuid)[0]
        user = fbu.user
        
        if( authenticate(username=user.username,"facebook")):
            login(request,user)
            
    #fb_data = parse_signed_request(request.POST.get('signed_request'))
    #logger.debug('Logging in FB user')
    #logger.debug(fb_data)
    #newuser = login_fb_user(fb_data)
    #if newuser:
    #   logger.debug("LOGIN: successfully logged in as "+str(request.user))
    #   login(request,newuser)
        return redirect(index)

def handle_fb_request(request):
    fb_data = parse_signed_request(request.POST.get('signed_request'))
    logger.debug('Registering FB user')
    logger.debug(fb_data)
    newuser = add_fb_user(fb_data)
    if newuser:
        logger.debug("REGISTER: successfully logged in as "+str(request.user))
        login(request,newuser)
    return redirect(index)


def request_fb_login():
    state = "zouf1234"
    args = {
        'client_id': FB_APP_ID,
        'redirect_uri': 'http://allsortz.com/handle_fb_login/',
        'state': state
    }
    url = 'https://www.facebook.com/dialog/oauth?' + \
            urllib.urlencode(args)
    
    raw_response = urllib.urlopen(url).read()
    response = cgi.parse_qs(raw_response)    
    
    if response:
        error = ''
        if response['access_token']:
            access_token = response['access_token'][0]
        if response['expires']:
            expires = response['expires'][0]
    else:
        access_token = 'No access token returned'
        expires = 'No expiration given'
        error = raw_response


def base64_url_decode(inp):
    inp = inp.replace('-','+').replace('_','/')
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.decodestring(inp)


def parse_signed_request(signed_request='a.a'):
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        print('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(FB_APP_SECRET, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        print('valid signed request received..')
        return data

def login_fb_user(fbdata):
    name = fbdata['registration']['name']
    email = fbdata['registration']['email']
    fbuser_id = fbdata['user_id']
    location = fbdata['registration']['location']
    try:
        u = User.objects.create(username=name,email=email)
    except:
        logger.error("Could not find user from the facebook auth")
    return authenticate(username=name,password="facebook")
    


def add_fb_user(fbdata):
    name = fbdata['registration']['name']
    email = fbdata['registration']['email']
    fbuser_id = fbdata['user_id']
    location = fbdata['registration']['location']
    try:
        u = User.objects.create(username=name,email=email)
        FacebookUser.objects.create(fbuser_id=fbuser_id,user=u)
    except:
        u = User.objects.get(username=name,email=email)
    u.set_password("facebook")
    u.save() 
    return authenticate(username=name,password="facebook")
