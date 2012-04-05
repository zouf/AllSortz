'''
Created on Apr 2, 2012

@author: Joey
'''

from django.contrib.auth.models import User
from ratings.models import Business, Rating
from random import Random

def createusers(n):
    for i in range(n):
        u = User.objects.create_user(username=("user" + str(i)));
        u.save()

def createbusinesses(n):
    for i in range(n):
        b = Business(name="business" + str(i), address="street" + str(i), city="princeton", state="NJ")
        b.save()

def addRandomRatings():
    r = Random();
    for user in User.objects.all():
        for business in Business.objects.all():
            rating = Random.randint(r, -1, 2)
            if rating==-1 : 
                rating = -2
            rat = Rating(business=business, username=user, rating=rating)
            rat.save()
