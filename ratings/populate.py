'''
Created on Apr 2, 2012

@author: Joey
'''

from django.contrib.auth.models import User
from ratings.models import Business, Rating

import random
from scipy.stats import norm
from numpy.random import binomial
import numpy
import scipy.stats

def getPdfOf(mu, stdev, x):
    return(1/((stdev)*numpy.sqrt(2*numpy.pi)) * numpy.exp(((-(x-mu))**2) * 1/(2*(stdev**2))))

def generateTest():
    # generate 2 binomials centered a a random business
    # one represents whether its been rated, the other what the rating was (like dislike)
    Rating.objects.all().delete()
    
    
    random.seed(666)
    
    NumBusiness = Business.objects.count()
    rating_given_sd = NumBusiness / 2
    pos_rating_sd = NumBusiness   / 4
    for user in User.objects.all():
        i = 0
        center = random.randint(0, NumBusiness-1)
        
        for business in Business.objects.all():
            
            norm_given_rat = scipy.stats.norm(center,rating_given_sd)
            prob_rat_given =   norm_given_rat.pdf(i)  *  1/norm_given_rat.pdf(center)
           # print('\n')
           # print("Mu is " + str(center))
           # print("pos_rating_stdev is " + str(rating_given_sd))
           # print("x is " + str(i))
           # print("Prob LHS " + str(prob_lhs))
           # print("Prob RHS " + str(prob_rhs))
           # print("result is " + str(prob_sel))
            
            rat_given_rv = binomial(1, prob_rat_given, size=1) #1 if rated, 0 otherwise
            if rat_given_rv[0] != 0:
                norm_pos_rat = scipy.stats.norm(center,pos_rating_sd)
                prob_pos_rat =  norm_pos_rat.pdf(i)  *  1/norm_pos_rat.pdf(center)
                pos_rat_rv = binomial(1, prob_pos_rat, size=1) #1 if positive, 0 negative
                rating_scaled = 0
                
                if pos_rat_rv[0] == 1:
                    rating_scaled = random.randint(3,5)
                else:
                    rating_scaled = random.randint(1,2)
                rat = Rating(business=business, username=user, rating=float(rating_scaled))
                rat.save()
            #no rating        
            i=i+1
        

def createusers(n):
    for i in range(n):
        queryset = User.objects.filter(username=("user" + str(i)))
        if queryset.count() >= 1:
            queryset.delete()
        u = User.objects.create_user(username=("user" + str(i)),password="test")
        u.save()

def createbusinesses(n):
    for i in range(n):
        queryset = Business.objects.filter(name="business" + str(i), address="street" + str(i), city="princeton", state="NJ")
        if queryset.count() >= 1:
            queryset.delete()
        b = Business(name="business" + str(i), address="street" + str(i), city="princeton", state="NJ",average_rating=-1)
        b.save()

def populate_test_data(numUsers, numBusinesses):
    Rating.objects.all().delete()
    User.objects.exclude(username="joey").exclude(username="zouf").delete()
    Business.objects.all().delete()
    createbusinesses(numBusinesses) 
    createusers(numUsers)
    generateTest()
    return
    