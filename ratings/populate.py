'''
Created on Apr 2, 2012

@author: Joey
'''

from django.contrib.auth.models import User
from ratings.models import Business, Rating, Keyword, Grouping
from recommendation.models import Recommendation, UserFactor, BusinessFactor


def create_user(username, uid):
    u = User(username=("u" + str(uid)), first_name=(username[0:20].encode("utf8")), password="")
    # u.set_password("test")
    return u


def create_category(name):
    k = Keyword(name=name)
    return k


def create_keyword(name):
    k = Keyword(name=name)
    k.save()
    return k


def create_keyword2bus(b, key):
    g = create_grouping(key, b)
    g.save()


def create_grouping(cat, bus):
    g = Grouping(business=bus, keyword=cat)
    return g


def create_rating(user, business, rating):
    r = Rating(username=user, business=business, rating=rating)
    return r


def create_business(name, address, state, city, lat, lon):
    b = Business(name=name.encode("utf8"), city=city.encode("utf8"), state=state, address=address.encode("utf8"), lat=lat, lon=lon, average_rating=0)
    return b


def clear_all_tables():
    Rating.objects.all().delete()
    User.objects.all().delete()
    Grouping.objects.all().delete()
    Keyword.objects.all().delete()
    Recommendation.objects.all().delete()
    #User.objects.exclude(username="joey").exclude(username="zouf").delete()
    User.objects.all().delete()
    Business.objects.all().delete()
    UserFactor.objects.all().delete()
    BusinessFactor.objects.all().delete()
