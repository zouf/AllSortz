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
 
import string

def create_user(username):
    #queryset = User.objects.filter(username=(username))
    #if queryset.count() >= 1:
    #    queryset.delete()

    u = User(username=(username.decode()),password="test")

    #u.save()
    return u
    

def create_rating(user,business,rating):
    #queryset = Rating.objects.filter(username=uid,business=bid)
    #if queryset.count() >=1:
    #    queryset.delete()
  #  queryuser= User.objects.filter(pk=uid)
   # querybusiness = Business.objects.filter(id=bid)

   
  
   # else:
   #     print(str(uid)+" Not found")
        
    return -1
    
    
def create_business(name, address, state, city, lat, lon):
    #queryset = Business.objects.filter(name=name, city=city, state=state)
    #if queryset.count >= 1:
    #    queryset.delete()
    b = Business(name=name.decode(),city=city.decode(),state=state.decode(),address=address.decode(),lat=lat,lon=lon,average_rating=0)
    #b.save()
    return b
 

def read_dataset():
    yelpUIDtoID = dict()
    yelpBIDtoID = dict()
    
    clear_all_tables()
    

    fp = open('/Users/zouf/Sites/nightout/data_import/michigan_dataset.json')
    #fp = open('C:\Users/Joey/nightout/data_import/michigan_dataset1.json')

    objs = json.load(fp)
    #pprint(objs)
    c=0;

    businesses = []
    users =[]
    
    unique_uid = 1
    unique_bid = 1
    print("json read\n");
    for o in objs:
        if(c%100==0):
            print(c)
        c=c+1
        if o['type'] == 'user':
            yelpID = o['user_id']
            name = "u"+str(c)
            u = create_user(name)           
            u.id = unique_uid
            users.append(u)
            unique_uid = unique_uid + 1
            #print(u)
            yelpUIDtoID[yelpID] = u 
        elif o['type'] == 'business':
            yelpID = o['business_id']
            name = "b"+str(c)
            state = "NY" #"o['state']
            longitude = o['longitude']
            latitude = o['latitude']
            full_address = "test st" #"o['full_address']
            city = "New York" #"o['city']
            b = create_business(name=name,address=full_address,state=state,city=city,lat=latitude,lon=longitude)
            b.id = unique_bid
            businesses.append(b)
            unique_bid = unique_bid + 1
            yelpBIDtoID[yelpID] = b
            
            
            
    User.objects.bulk_create(users)
    Business.objects.bulk_create(businesses)
    c=0
    print("Users and businesses read");
    ratings = []
    for o in objs:
        if(c%100==0):
            print(c)
        c=c+1
        if o['type']=='review':
            uid = o['user_id']
            bid = o['business_id']
            stars = o['stars']
            if uid  in yelpUIDtoID:
                if bid in yelpBIDtoID:
                    usr = yelpUIDtoID[uid]
                    bus = yelpBIDtoID[bid]
                    r = Rating(username=usr, business=bus, rating=stars)
                    ratings.append(r)
    Rating.objects.bulk_create(ratings)
    transaction.commit();
    
