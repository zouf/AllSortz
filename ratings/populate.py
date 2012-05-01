'''
Created on Apr 2, 2012

@author: Joey
'''

from django.contrib.auth.models import User
from ratings.models import Business, Rating

import random
from scipy.stats import norm
from numpy.random import binomial
from numpy import dot
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
        u = create_user("tst"+str(i))
        u.id = i        
        u.save()

def  createbusinesses(n):
    for i in range(1,n):
        b =  create_business('b'+str(i), "tst", "NY", "tst", 0, 0)
        b.id = i
        b.save()
        

def generate_nmf_test(numFactors, density):
    allUsers = User.objects.all()
    allBusinsses = Business.objects.all()
    random.seed(666)
    newP = []
    for u in range(0,allUsers.count()):
        if u not in newP:
            newP.append([])
        for k in range(0,numFactors):
            rif = random.uniform(0,1)
            newP[u].append(rif)
    
    newQ = []     
    for k in range(0,numFactors):
        newQ.append([])
        for j in range(0,allBusinsses.count()):
            rif = random.uniform(0,1)
            newQ[k].append(rif)
    
    initR = dot(newP,newQ)
    
    i = 0
    for u in allUsers:
        j = 0
        for b in allBusinsses:
            chance = random.uniform(0,1)
            if(chance < density):
                rat = Rating(business=b, username=u, rating=float(initR[i][j]))
                rat.save()
            j = j + 1
    i = i + 1
    
def create_user(username):
    u = User(username=(username.decode()),password="test")
    return u
    

def create_rating(user,business,rating):
    r = Rating(username=user, business=business, rating=rating)
    return r
    
    
def create_business(name, address, state, city, lat, lon):
    b = Business(name=name.decode(),city=city.decode(),state=state.decode(),address=address.decode(),lat=lat,lon=lon,average_rating=0)
    return b
 

    
def pop_test_user_bus_data(numUsers, numBusinesses):
    Rating.objects.all().delete()
    User.objects.exclude(username="joey").exclude(username="zouf").delete()
    Business.objects.all().delete()
    createbusinesses(numBusinesses) 
    createusers(numUsers)   
    return
    

def clear_all_tables():
    Rating.objects.all().delete()
    User.objects.all().delete()
    #User.objects.exclude(username="joey").exclude(username="zouf").delete()
    Business.objects.all().delete()
    
def populate_test_data(numUsers, numBusinesses):
    Rating.objects.all().delete()
    User.objects.exclude(username="joey").exclude(username="zouf").delete()
    Business.objects.all().delete()
    createbusinesses(numBusinesses) 
    createusers(numUsers)
    generateTest()
    return
    