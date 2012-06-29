'''
Created on Apr 2, 2012

@author: Joey
'''
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from photos.models import BusinessPhoto
from rateout import settings
from ratings.models import Business, Rating
from recommendation.models import Recommendation, UserFactor, BusinessFactor
from tags.models import Tag, HardTag
from urllib import urlretrieve
from usertraits.models import Trait
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
       
        name = row[0]
        descr = row[1]

        print('tag name: '+str(name))
        print('tag descr: '+str(descr))
        
        t = Tag(name=name,descr=descr)
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

        print('trait name: '+str(name))
        print('trait descr: '+str(descr))
        
        t = Trait(name=name,descr=descr)
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
        
        t = HardTag(descr=descr,question=question)
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
        
        b = Business(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=addr.encode("utf8"), lat=0, lon=0)
        b.save()
        outpath =settings.STATIC_ROOT+'img'+str(i)+'.jpg'
        

        #print('retrieve'+str(urlparse.urlunparse(phurl)))
        urlretrieve(phurl, outpath)
        bp = BusinessPhoto(user=user, business=b, image=outpath, title="test main", caption="test cap")
        try:
            bp.save()
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            pass
            


def prepopulate_database(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
    if request.user.username != 'zouf':
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)

    
    prepop_businesses(request.user)
    prepop_sorts(request.user)
    prepop_traits(request.user)
    prepop_questions(request.user)
   
        
    return HttpResponseRedirect('/')

    

def create_rating(user, business, rating):
    r = Rating(username=user, business=business, rating=rating)
    return r


def create_business(name, address, state, city, lat, lon):
    b = Business(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=address.encode("utf8"), lat=lat, lon=lon)
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
