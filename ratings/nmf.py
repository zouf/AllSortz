
from celery.decorators import task
import logging
import math
import random
import scipy

import numpy
import sys
from celery.decorators import periodic_task
from datetime import timedelta
from ratings.models import Business
from ratings.models import Rating
from ratings.models import DontCare
from ratings.models import Recommendation
from django.contrib.auth.models import User
from ratings.models import Business
from ratings.models import Rating


def get_for_fold_new(f):
    ratingTable = dict()
    allBusinesses = Business.objects.all()
    numBusinesses = allBusinesses.count()
    
    
    allUsers = User.objects.all()
    numUsers = allUsers.count()
    
    allRatings = Rating.objects.all()
    inFoldData = []
    id2bus = dict()
    id2usr = dict()
    
    inMemRat = dict()
    
   # ratAsArray = numpy.empty((numUsers,numBusinesses))
    ratAsArray = numpy.empty((numUsers,numBusinesses),dtype=numpy.uint8)
    print(numUsers)
    print(numBusinesses)
    ratAsArray.fill(0)
    ctr = 0
    for r in allRatings:
        if ctr % 500 == 0:
            print(ctr)
        ctr = ctr + 1
        uid = r.username.id
        bid = r.business.id
        foldId = random.randint(1,5)
        if foldId == f:
            ratAsArray[uid-1][bid-1] = 0
            inFoldData.append(r)
        else:
            try:
                ratAsArray[uid-1][bid-1] = r.rating 
            except:
                print(uid)
                print(bid) 
    print(ratAsArray)   
    sys.exit()
    
    
def get_for_fold(f):
    ratingTable = dict()
    allBusinesses = Business.objects.all()
    numBusinesses = allBusinesses.count()
    
    
    allUsers = User.objects.all()
    numUsers = allUsers.count()
    
    allRatings = Rating.objects.all()
    inFoldData = []
    id2bus = dict()
    id2usr = dict()
    
    
    random.seed = 666
    i = 0
 
    for u in allUsers:
        
        j = 0
        ratingTable[i] = {}
        id2usr[u] = i
        for b in allBusinesses:
            
        #    print(b)
            id2bus[b] = j
            if u in inMemRat:
                if b in inMemRat[u]:
                    foldId = random.randint(1,5)
                    r = allRatings.values(username=u, business=b)
                    if foldId == f:
                        ratingTable[i][j] = 0
                        inFoldData.append(r)
                    else:
                        ratingTable[i][j] = r.rating                
                else:
                    ratingTable[i][j] = 0
            else:
                ratingTable[i][j] = 0
            j=j+1
        i=i+1
    return ratingTable, inFoldData, id2usr, id2bus
 

def test_matrix_fact():
    N = User.objects.count()
    M = Business.objects.count()
    allRatings = Rating.objects.all()
    nR = run_nmf_internal(allRatings,N,M, 2)


def get_rating_folds():
    #loop over K
    for k in range(1,15,3):
        
        sumDist = 0
        for f in range(1,6): 
            print("Running for fold "+str(f))
            ratingTable,inFoldData,id2usr,id2bus = get_for_fold(f)
            
            nR = run_nmf_internal(ratingTable, k)
            # call matrix factorization
            dist = 0
            for r in inFoldData:
                #print("Username " + str(r.username))
                #print("Business " + str(r.business.name))
                #print("Rating " + str(r.rating))
                user = r.username
                business = r.business
                rat = r.rating
                prediction = nR[id2usr[user]][id2bus[business]]
                #print("Prediction " + str(prediction))
                #print("")
                #print("")
                dist = dist + math.pow(abs(float(prediction) - float(rat)),2)
            sumDist = sumDist + dist / len(inFoldData)
            print("For fold = "+str(f)+" dist = "+str(dist/len(inFoldData)))
        print("Average Distance for K= "+str(k) + " is " + str(sumDist/5))
        
        
  
 # http://www.albertauyeung.com/mf.php
def matrix_factorization(R, P, Q, K, steps=2, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        print("Beginning step"+str(step))
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
                print("\t\tOne iteration of small-ass loop: "+str(j))
            print("\tOne iteration of big-ass loop: "+str(i))
        eR = numpy.dot(P,Q)
        
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    return P, Q.T



def matrix_factorization_new(allRatings,  P, Q, K, steps=2, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        ct = 0
        for r in allRatings:
            uid = r.username.id -1
            bid = r.business.id -1
            eij = r.rating - numpy.dot(P[uid,:],Q[:,bid])
        
            for k in xrange(K):
                P[uid][k] = P[uid][k] + alpha * (2 * eij * Q[k][bid] - beta * P[uid][k])
                Q[k][bid] = Q[k][bid] + alpha * (2 * eij * P[uid][k] - beta * Q[k][bid])
            if ct % 100 == 0:
                print(ct)
            ct = ct + 1
        print("First loop done")
        eR = numpy.dot(P,Q)
        e = 0
        for r in allRatings:
            uid = r.username.id -1
            bid = r.business.id -1
            eij = r.rating - numpy.dot(P[uid,:],Q[:,bid])
            e = e + pow(r.rating - numpy.dot(P[uid,:],Q[:,bid]), 2)
            for k in xrange(K):
                e = e + (beta/2) * (pow(P[uid][k],2) + pow(Q[k][bid],2))
        if e < 0.001:
            break
    return P, Q.T



def run_nmf_internal(R,N,M, K):
    
    

    
    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)
     
    nP, nQ = matrix_factorization_new(R, P, Q, K)
    nR = numpy.dot(nP, nQ.T)

    return nR
