'''
Created on Apr 2, 2012

@author: Joey
'''
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from photos.models import BusinessPhoto
from photos.views import add_photo_by_url
from queries.models import Query
from rateout import settings
from ratings.models import Business, Rating
from ratings.utility import setBusLatLng
from tags.models import Tag, HardTag, ValueTag
from tags.views import add_tag_to_bus, get_master_summary_tag, get_default_user
from usertraits.models import Trait
import csv
import logging

logger = logging.getLogger(__name__)
def create_user(username, uid):
    u = User(username=("u" + str(uid)), first_name=(username[0:20].encode("utf8")), password="")
    # u.set_password("test")
    return u


def prepop_sorts(user):
    reader = csv.reader(open(settings.BASE_DIR+'/prepop/sorts.csv', 'U'), delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue
       
        descr = row[0]
        icon = row[1]

        tset = Tag.objects.filter(descr=descr)
        if tset.count() > 0:
            continue
             
        t = Tag(descr=descr,creator=user,icon=icon)
        t.save()
        
        
def prepop_traits(user):
    reader = csv.reader(open(settings.BASE_DIR+'/prepop/traits.csv', 'U'), delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue
       
        name = row[0]
        descr = row[1]

        print('Trait name: '+str(name))
        print('trait descr: '+str(descr))
        
        tset = Trait.objects.filter(name=name)
        if tset.count() > 0:
            continue
        
        t = Trait(name=name,descr=descr,creator=user)
        t.save()


            
        
        

def prepop_questions(user):
    reader = csv.reader(open(settings.BASE_DIR+'/prepop/questions.csv', 'U'), delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue
       
        question = row[0]
        descr = row[1]
        tagtype = row[2]
        print('tag question: '+str(question))
        print('tag descr: '+str(descr))
        
        
        if tagtype == 'boolean':
            
            tset = HardTag.objects.filter(question=question)
            if tset.count() > 0:
                continue
            
            t = HardTag(descr=descr,question=question,creator=user)
            t.save()
        elif tagtype=='integer':
            tset = ValueTag.objects.filter(question=question)
            if tset.count() > 0:
                continue
            
            t = ValueTag(descr=descr,question=question,creator=user)
            t.save()
        
        
        

def prepop_businesses(user):
    if user == None:
        user = get_default_user()
    reader = csv.reader(open(settings.BASE_DIR+'/prepop/businesses.csv', 'U'), delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue
    
        name = row[0]
        addr = row[1]
        city = row[2]
        state = row[3]
        phurl = row[4]
        print('name: '+str(name))
        print('addr: '+str(addr))
        print('city: '+str(city))
        print('state: '+str(state))
        
        
        bset = Business.objects.filter(name=name,address=addr,state=state,city=city)
        if bset.count() == 0:
            b = Business(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=addr.encode("utf8"), lat=0, lon=0)
            b.save()
        elif bset.count() > 1:
            Business.objects.filter(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=addr.encode("utf8")).delete()
            b = Business(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=addr.encode("utf8"), lat=0, lon=0)
            b.save()
        else:
            b = bset[0]
            
        setBusLatLng(b)        
        add_tag_to_bus(b, get_master_summary_tag(), get_default_user())
        add_photo_by_url(phurl,b,user,default=True)

def prepop_queries(user):
    user = get_default_user()
    for t in Tag.objects.all():
        q = Query(name=t.descr,proximity=5,value=5,score=5,price=5,visited=False,deal=False,networked=False,text="",creator=user,is_default=True)
        q.save()
        
def prepopulate_database(request):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    #if request.user.username != 'zouf':
    #    return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
    
#    UNCOMMENT TO DELETE

    #Business.objects.all().delete()
#    BusinessPhoto.objects.all().delete()
#    Comment.objects.all().delete()
#    BusinessTag.objects.all().delete()
#    TagComment.objects.all().delete()
#    Page.objects.all().delete()
#    PageRelationship.objects.all().delete()
#    HardTag.objects.all().delete()
#    ValueTag.objects.all().delete()
#    Tag.objects.all().delete()
#    Trait.objects.all().delete()
#    
    prepop_businesses(request.user)
    prepop_sorts(request.user)
    prepop_traits(request.user)
    prepop_questions(request.user)
    prepop_queries(request.user)
    return HttpResponseRedirect('/')

    

def create_rating(user, business, rating):
    r = Rating(username=user, business=business, rating=rating)
    return r


def create_business(name, address, state, city, lat, lon):
    bset = Business.objects.filter(name=name,address=address,state=state,city=city)
    if bset.count() > 0:
        return
    
    b = Business(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=address.encode("utf8"), lat=lat, lon=lon)
    b.save()
    
    setBusLatLng(b)
    add_tag_to_bus(b,get_master_summary_tag())
    return b
        


