# Create your views here.
from communities.models import UserMembership, Community
import logging


logger = logging.getLogger(__name__)

def get_default():
    try:
        c = Community.objects.get(name="Princeton")
    except:
        logger.debug("Creating a default community of Princeton")
        c = Community(name="Princeton", descr="Default Community of Princeton", city="Princeton")
        c.save()
    return c

def get_community(user):
    if user.is_authenticated():
        try:
            membership = UserMembership.objects.get(user=user,default=True)
            return membership.community
        except:
        #TODO change to be based on browser location
            return get_default()
    return get_default()
        
