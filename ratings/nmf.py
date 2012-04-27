
from celery.decorators import task
import logging
import math
import random
import scipy
import numpy

from celery.decorators import periodic_task
from datetime import timedelta
from ratings.models import Business
from ratings.models import Rating
from ratings.models import DontCare
from ratings.models import Recommendation
from django.contrib.auth.models import User
from ratings.models import Business
from ratings.models import Rating



def get_for_fold(f):
    ratingTable = dict()
    allBusinesses = Business.objects.all()
    allUsers = User.objects.all()
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
            r = Rating.objects.filter(username=u, business=b)
            if r:
                foldId = random.randint(1,5)
                r = Rating.objects.get(username=u, business=b)
                if foldId == f:
                    ratingTable[i][j] = 0
                    inFoldData.append(r)
                else:
                    ratingTable[i][j] = r.rating                
            else:
                ratingTable[i][j] = 0
            j=j+1
        i=i+1
    return ratingTable, inFoldData, id2usr, id2bus
 


def get_rating_folds():
    #loop over K
    for k in range(1,15,3):
        
        sumDist = 0
        for f in range(1,6): 
            ratingTable,inFoldData,id2usr,id2bus = get_for_fold(f)
            nR = run_nmf(ratingTable, k)
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
def matrix_factorization(R, P, Q, K, steps=50, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
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


def run_nmf(R,K):
    
    N = len(R)
    M = len(R[0])
    
    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)
     
    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = numpy.dot(nP, nQ.T)

    return nR
