# Create your views here.

from communities.models import UserMembership, Community
import logging


logger = logging.getLogger(__name__)

def get_default():
    cfilter = Community.objects.filter(name="Princeton")
    if cfilter.count() == 0:
        logger.debug("Creating a default community of Princeton")
        c = Community(name="Princeton", descr="Default Community of Princeton", city="Princeton",state="NJ")
        c.save()
        return c
    else:
        return cfilter[0]

def get_community(user):
    if not user:
        return get_default()
    if user.is_authenticated():
        try:
            membership = UserMembership.objects.get(user=user,default=True)
            return membership.community
        except:
        #TODO change to be based on browser location
            return get_default()
    return get_default()
        


def test_func2():
    return False
