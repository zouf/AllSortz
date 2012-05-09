'''
Created on Apr 30, 2012

@author: zouf
'''
from django.conf import settings
from pprint import pprint 
from django.db import transaction
from django.db.models.aggregates import Count
from ratings.models import Business, Rating, User, Keyword, Grouping
from ratings.populate import create_business, create_rating, create_user, \
    create_grouping, clear_all_tables, create_category, create_grouping
from ratings.normalization import buildAverageRatings
import simplejson as json

bus_rating_threshold = 50
user_rating_threshold = 10


def read_dataset():
    yelpUIDtoID = dict()
    yelpBIDtoID = dict()
    clear_all_tables()
    fp = open(settings.DATASET_LOCATION)
    #fp = open('C:\Users/Joey/nightout/data_import/michigan_dataset1.json')

    objs = json.load(fp)
    #pprint(objs)

    businesses = []
    users =[]
    
    cats2bus = dict()
    uniquecats = dict()
    
    unique_uid = 1
    unique_bid = 1

    global bus_rating_threshold
    global user_rating_threshold
    
    print("json read\n");
    c=0;
    for o in objs:
        if(c%100==0):
            print(c)
        c=c+1
        if o['type'] == 'user':
            yelpID = o['user_id']
            #name = "u"+str(c)
            name = o['name']
            rev_count = o['review_count']
            if rev_count < user_rating_threshold:
                continue
            u = create_user(name,unique_uid)           
            u.id = unique_uid
            users.append(u)
            unique_uid = unique_uid + 1
            #u.save()
            #print(u)
            yelpUIDtoID[yelpID] = u 
    User.objects.bulk_create(users)
    business_set = set()
    for o in objs:
        if o['type'] == 'review':
            uid = o['user_id']
            bid = o['business_id']
            if uid in yelpUIDtoID:
                if bid not in business_set:
                    business_set.add(bid)
    for o in objs:
        if o['type'] == 'business':
            yelpID = o['business_id']
            if yelpID in business_set:
                rev_count = o['review_count']
    
                if rev_count < bus_rating_threshold:
                    continue

                cats = o['categories']
            
                
                name = o['name']
                state =  o['state']
                longitude = o['longitude']
                latitude = o['latitude']
                full_address = o['full_address']
                city = o['city']
                b = create_business(name=name,address=full_address,state=state,city=city,lat=latitude,lon=longitude)
                b.id = unique_bid
                cats2bus[b] = []
                for append_cat in cats:
                    if append_cat not in uniquecats:
                        uniquecats[append_cat] = 1
                    cats2bus[b].append(append_cat)
                businesses.append(b)
                unique_bid = unique_bid + 1
                yelpBIDtoID[yelpID] = b       
   
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

 #   create_cat_list = []
    cat_name_to_obj = {}
    for cat_name in uniquecats:
        k = create_category(name=cat_name)
        k.save()
        cat_name_to_obj[cat_name] = k
  #      create_cat_list.append(k)
  #  Keyword.objects.bulk_create(create_cat_list)
    
    create_grouping_list = []
    for b in Business.objects.all():
        for cat_name in cats2bus[b]:
            g = create_grouping(cat_name_to_obj[cat_name],b)
            create_grouping_list.append(g)
    Grouping.objects.bulk_create(create_grouping_list)
    transaction.commit();
    pare_dataset()
    buildAverageRatings()

def pare_dataset():
    # All the ratings are in the DB at this point, out of laziness we now
    # go through again and delete any user that doesn't have enough reviews
    # for the businesses that actually got added
  print("Ratings before - "+str(Rating.objects.count()))

  numRatings = Rating.objects.count()
  numUsers  = User.objects.count()
  numBusinesses = Business.objects.count()
  print("Average ratings/user = " + str(numRatings/numUsers) + " avg rat / bus is " + str(numRatings / numBusinesses))   

  usrs = User.objects.all()
#  for u in usrs:
#    c = Rating.objects.filter(username=u.id).aggregate(Count('rating'))
#    if c['rating__count'] < user_rating_threshold:
#      Rating.objects.filter(username=u.id).delete()
#      u.delete()
  print("Ratings after user delete - "+str(Rating.objects.count()))
  businesses = Business.objects.all()
  for b in businesses:
    c = Rating.objects.filter(business=b.id).aggregate(Count('rating'))
    if c['rating__count'] < bus_rating_threshold / 10:
      Rating.objects.filter(business=b.id).delete()
      b.delete()
      #c.delete()
  

  
  print("Ratings after bus delete - "+str(Rating.objects.count()))

