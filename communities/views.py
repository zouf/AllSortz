# Create your views here.
from communities.models import UserMembership, Community


def get_community(user):
    if user.is_authenticated():
        try:
            membership = UserMembership.objects.get(user=user,default=True)
            community = membership.community
        except:
        #TODO change to be based on browser location
            community = Community.objects.get(name="Princeton")
        return community
    return Community.objects.get(name="Princeton")
        
