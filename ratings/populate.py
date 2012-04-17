'''
Created on Apr 2, 2012

@author: Joey
'''

from django.contrib.auth.models import User
from ratings.models import Business, Rating
from random import Random


def generateTest():
    # generate 2 binomials centered a a random business
    # one represents whether its been rated, the other what the rating was (like dislike)
    


def createusers(n):
    for i in range(n):
        queryset = User.objects.filter(username=("user" + str(i)))
        if queryset.count() >= 1:
            queryset.delete()
        u = User.objects.create_user(username=("user" + str(i)))
        u.save()

def createbusinesses(n):
    for i in range(n):
        queryset = Business.objects.filter(name="business" + str(i), address="street" + str(i), city="princeton", state="NJ")
        if queryset.count() >= 1:
            queryset.delete()
        b = Business(name="business" + str(i), address="street" + str(i), city="princeton", state="NJ")
        b.save()

def addRandomRatings():
    r = Random();
    for user in User.objects.all():
        for business in Business.objects.all():
            rating = Random.randint(r, -1, 2)
            queryset = Rating.objects.filter(username=user, business=business)
            if queryset.count() >= 1:
                queryset.delete()
            
            if rating==-1 : 
                rating = -2
            rat = Rating(business=business, username=user, rating=rating)
            rat.save()


def populate_test_data(numUsers, numBusinesses):
   # createusers(numUsers)
    createbusinesses(numBusinesses) 
    addRandomRatings()
    return
    