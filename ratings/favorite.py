'''
Created on Jun 28, 2012

@author: zouf
'''
from ratings.models import UserFavorite





    
def get_user_favorites(user):
    favorites = []
    for f in UserFavorite.objects.all():
        favorites.append(f.business)
    return favorites

def is_user_subscribed(b,user):
    if user and UserFavorite.objects.filter(business=b,user=user).count() >0:
        return True;
    return False