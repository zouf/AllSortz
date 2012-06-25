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
    facebook_data = parse_signed_request(request.POST.get('signed_request'))
    logger.debug('zouf----')
    logger.debug(facebook_data['fb_data'])

def handle_fb_request(request):
    facebook_data = parse_signed_request(request.POST.get('signed_request'))
    logger.debug('zouf----')
    logger.debug(facebook_data['fb_data'])
    add_fb_user(facebook_data['fb_data'])


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


def add_fb_user(fbdata):
    name = fbdata['registration']['name']
    email = fbdata['registration']['email']
    fbuser_id = fbdata['user']['user_id']
    location = fbdata['registration']['location']
    u = User.objects.create(name=name,email=email)
    fbuser = FacebookUser.objects.create(fbuser_id=fbuser_id,user=u)