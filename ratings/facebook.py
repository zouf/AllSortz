'''
Created on Jun 25, 2012

@author: zouf
'''
from django.contrib.auth.models import User
from rateout.settings import FB_APP_SECRET
from ratings.models import FacebookUser
import base64
import hashlib
import hmac
import json
import logging


logger = logging.getLogger(__name__)

def handle_fb_login(request):
    logger.debug("zouflogin")
    facebook_data = fb_request_decode(request.POST.get('signed_request'))
    logger.debug('zouf----')
    logger.debug(facebook_data['fb_data'])

def handle_fb_request(request):
    facebook_data = fb_request_decode(request.POST.get('signed_request'))
    logger.debug('zouf----')
    logger.debug(facebook_data['fb_data'])
    add_fb_user(facebook_data['fb_data'])


def fb_request_decode(signed_request):
    s = [s.encode('ascii') for s in signed_request.split('.')]
    fb_sig = base64.urlsafe_b64decode(s[0] + '=')
    logger.debug(base64.decodestring(s[1]))
    fb_data = json.loads(base64.decodestring(s[1]))#base64.urlsafe_b64decode(s[1]))
    fb_hash = hmac.new(FB_APP_SECRET, s[1], hashlib.sha256).digest()

    sig_match = False
    if fb_sig == fb_hash:
        sig_match = True

    auth = False
    if 'user_id' in fb_data:
        auth = True

    return {
        'fb_sig' : fb_sig,
        'fb_data' : fb_data,
        'fb_hash' : fb_hash,
        'sig_match' : sig_match,
        'auth' : auth,
    }


def add_fb_user(fbdata):
    name = fbdata['registration']['name']
    email = fbdata['registration']['email']
    fbuser_id = fbdata['user']['user_id']
    location = fbdata['registration']['location']
    u = User.objects.create(name=name,email=email)
    fbuser = FacebookUser.objects.create(fbuser_id=fbuser_id,user=u)