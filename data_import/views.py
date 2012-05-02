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
from ratings.populate import  create_user
from ratings.populate import  create_rating
from ratings.populate import  create_business
from ratings.populate import clear_all_tables
 

def read_dataset():
    yelpUIDtoID = dict()
    yelpBIDtoID = dict()
    clear_all_tables()
    fp = open('/Users/zouf/Sites/nightout/data_import/michigan_dataset.json')
    #fp = open('C:\Users/Joey/nightout/data_import/michigan_dataset1.json')

    objs = json.load(fp)
    #pprint(objs)

    businesses = []
    users =[]
    
    unique_uid = 1
    unique_bid = 1
    bus_rating_threshold = 100
    user_rating_threshold = 25
    
    print("json read\n");
    c=0;
    for o in objs:
        if(c%100==0):
            print(c)
        c=c+1
        if o['type'] == 'user':
            yelpID = o['user_id']
            name = "u"+str(c)
            rev_count = o['review_count']
            if rev_count < user_rating_threshold:
                continue
            u = create_user(name)           
            u.id = unique_uid
            users.append(u)
            unique_uid = unique_uid + 1
            #print(u)
            yelpUIDtoID[yelpID] = u 
        elif o['type'] == 'business':
            yelpID = o['business_id']
            rev_count = o['review_count']
            if rev_count < bus_rating_threshold:
                continue
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
                    r = create_rating(usr, bus, stars)
                    ratings.append(r)
    Rating.objects.bulk_create(ratings)
    transaction.commit();
    
