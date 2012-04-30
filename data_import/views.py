'''
Created on Apr 30, 2012

@author: zouf
'''
import simplejson as json
from pprint import pprint
from ratings.models import User
from ratings.models import Business
from ratings.models import Rating
from django.db import transaction
from ratings.populate import clear_all_tables


def create_user(username):
    #queryset = User.objects.filter(username=(username))
    #if queryset.count() >= 1:
    #    queryset.delete()
    u = User(username=(username),password="test")
    #u.save()
    return u
    

def create_rating(uid,bid,rating):
    #queryset = Rating.objects.filter(username=uid,business=bid)
    #if queryset.count() >=1:
    #    queryset.delete()
    use = User.objects.get(pk=uid);
    bus = Business.objects.get(id=bid)
    r = Rating(username=use,business=bus, rating=rating)
    #r.save()
    return r
    
    
def create_business(name, address, state, city, lat, lon):
    #queryset = Business.objects.filter(name=name, city=city, state=state)
    #if queryset.count >= 1:
    #    queryset.delete()
    b = Business(name=name,city=city,state=state,address=address,lat=lat,lon=lon,average_rating=0)
    #b.save()
    return b
 

def read_dataset():
    yelpUIDtoID = dict()
    yelpBIDtoID = dict()
    
    clear_all_tables()
    
    #fp = open('/Users/zouf/Sites/nightout/data_import/little.json')
    fp = open('C:\Users/Joey/nightout/data_import/michigan_dataset1.json')
    objs = json.load(fp)
    #pprint(objs)
    c=0;
    businesses = []
    users =[]
    print("json read\n");
    for o in objs:
        if(c%100==0):
            print(c)
        c=c+1
        if o['type'] == 'user':
            yelpID = o['user_id']
            name = o['name']
            u = create_user(name)
            ourID = u.pk
            users.append(u)
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
            businesses.append(b)
            yelpBIDtoID[yelpID] = b.id
            
    User.objects.bulk_create(users)
    Business.objects.bulk_create(businesses)
    c=0
    print("Users and businesses read");
    for o in objs:
        if(c%100==0):
            print(c)
        c=c+1
        if o['type']=='review':
            uid = o['user_id']
            bid = o['business_id']
            stars = o['stars']
            create_rating(uid=yelpUIDtoID[uid], bid=yelpBIDtoID[bid],rating=stars)
    transaction.commit();
