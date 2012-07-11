'''
Created on Apr 2, 2012

@author: Joey
'''
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from photos.models import BusinessPhoto
from rateout import settings
from ratings.models import Business, Rating, Comment, TagComment, \
    PageRelationship
from recommendation.models import Recommendation, UserFactor, BusinessFactor
from tags.models import Tag, HardTag, BusinessTag
from tags.views import add_tag_to_bus, get_master_summary_tag, get_default_user
from urllib import urlretrieve
from usertraits.models import Trait
from wiki.models import Page
import csv
import logging
import string
import sys
import urlparse

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

        print('Tag name: '+str(descr))   
        
        tset = Tag.objects.filter(descr=descr)
        if tset.count() > 0:
            continue
             
        t = Tag(descr=descr,creator=user)
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
        print('tag question: '+str(question))
        print('tag descr: '+str(descr))
        
        tset = HardTag.objects.filter(question=question)
        if tset.count() > 0:
            continue
        
        t = HardTag(descr=descr,question=question,creator=user)
        t.save()

def prepop_businesses(user):

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
        
        b = Business.objects.get(name=name)
        
        add_tag_to_bus(b, get_master_summary_tag(), get_default_user())
        outpath =settings.STATIC_ROOT+'img'+str(i)+'.jpg'
        

        #print('retrieve'+str(urlparse.urlunparse(phurl)))
        urlretrieve(phurl, outpath)
        bp = BusinessPhoto(user=user, business=b, image=outpath, title="test main", caption="test cap")
        try:
            bp.save(False)
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            pass
            


def prepopulate_database(request):

    if not request.user.is_superuser:
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    #if request.user.username != 'zouf':
    #    return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
    
#    UNCOMMENT TO DELETE

    Business.objects.all().delete()
    BusinessPhoto.objects.all().delete()
#    Comment.objects.all().delete()
#    BusinessTag.objects.all().delete()
#    TagComment.objects.all().delete()
#    Page.objects.all().delete()
#    PageRelationship.objects.all().delete()
#    
    
#    HardTag.objects.all().delete()
#    Tag.objects.all().delete()
#    Trait.objects.all().delete()
#    
    prepop_businesses(request.user)
    prepop_sorts(request.user)
    prepop_traits(request.user)
    prepop_questions(request.user)
   
        
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
        


def clear_all_tables():
    Rating.objects.all().delete()
    User.objects.all().delete()
    Recommendation.objects.all().delete()
    #User.objects.exclude(username="joey").exclude(username="zouf").delete()
    User.objects.all().delete()
    Business.objects.all().delete()
    UserFactor.objects.all().delete()
    BusinessFactor.objects.all().delete()
