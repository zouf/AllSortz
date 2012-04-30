'''
Created on Apr 30, 2012

@author: zouf
'''
import simplejson as json
from pprint import pprint
from ratings.models import User
from ratings.models import Business
from ratings.models import Rating


def create_user(username):
    queryset = User.objects.filter(username=(username))
    if queryset.count() >= 1:
        queryset.delete()
    u = User.objects.create_user(username=(username),password="test")
    u.save()
    return u.pk
    
def create_rating(uid,bid,rating):
    queryset = Rating.objects.filter(username=uid,business=bid)
    if queryset.count() >=1:
        queryset.delete()
    r = Rating.objects.create(username=uid,business=bid, rating=rating)
    r.save()
    
    
def create_business(name, address, state, city, lat, lon):
    queryset = Business.objects.filter(name=name, city=city, state=state)
    if queryset.count >= 1:
        queryset.delete()
    b = Business.objects.create(name=name,city=city,state=state,address=address,lat=lat,lon=lon,average_rating=0)
    b.save()
    return b
    
def read_dataset():
    yelpUIDtoID = dict()
    yelpBIDtoID = dict()
    
    fp = open('/Users/zouf/Sites/nightout/data_import/little.json')
    objs = json.load(fp)
    pprint(objs)
    for o in objs:

        if o['type'] == 'user':
            yelpID = o['user_id']
            name = o['name']
            ourID = create_user(name)
            yelpUIDtoID[yelpID] = ourID
        elif o['type'] == 'business':
            yelpID = o['business_id']
            name = o['name']
            state = o['state']
            longitude = o['longitude']
            latitude = o['latitude']
            full_address = o['full_address']
            city = o['city']
            b = create_business(name=name,address=full_address,state=state,city=city,lat=latitude,lon=longitude)
            yelpBIDtoID[yelpID] = b.id

    for o in objs:
        if o['type']=='review':
            uid = o['user_id']
            bid = o['business_id']
            stars = o['stars']
            create_rating(uid=yelpUIDtoID[uid], bid=yelpBIDtoID[bid],rating=stars)

