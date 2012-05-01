
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
import fastnmf




#def get_for_fold_new(f):
#    ratingTable = dict()
#    allBusinesses = Business.objects.all()
#    numBusinesses = allBusinesses.count()
#    
#    
#    allUsers = User.objects.all()
#    numUsers = allUsers.count()
#    
#    allRatings = Rating.objects.all()
#    inFoldData = []
#    id2bus = dict()
#    id2usr = dict()
#    
#    inMemRat = dict()
#    
#   # ratAsArray = numpy.empty((numUsers,numBusinesses))
#    ratAsArray = numpy.empty((numUsers,numBusinesses),dtype=numpy.uint8)
#    print(numUsers)
#    print(numBusinesses)
#    ratAsArray.fill(0)
#    ctr = 0
#    for r in allRatings:
#        if ctr % 500 == 0:
#            print(ctr)
#        ctr = ctr + 1
#        uid = r.username.id
#        bid = r.business.id
#        foldId = random.randint(1,5)
#        if foldId == f:
#            ratAsArray[uid-1][bid-1] = 0
#            inFoldData.append(r)
#        else:
#            try:
#                ratAsArray[uid-1][bid-1] = r.rating 
#            except:
#                print(uid)
#                print(bid) 
#    print(ratAsArray)   
#    sys.exit()
#    
    
#def get_for_fold(f):
#    ratingTable = dict()
#    allBusinesses = Business.objects.all()
#    numBusinesses = allBusinesses.count()
#    
#    
#    allUsers = User.objects.all()
#    numUsers = allUsers.count()
#    
#    allRatings = Rating.objects.all()
#    inFoldData = []
#    id2bus = dict()
#    id2usr = dict()
#    
#    
#    random.seed = 666
#    i = 0
# 
#    for u in allUsers:
#        
#        j = 0
#        ratingTable[i] = {}
#        id2usr[u] = i
#        for b in allBusinesses:
#            
#        #    print(b)
#            id2bus[b] = j
#            if u in inMemRat:
#                if b in inMemRat[u]:
#                    foldId = random.randint(1,5)
#                    r = allRatings.values(username=u, business=b)
#                    if foldId == f:
#                        ratingTable[i][j] = 0
#                        inFoldData.append(r)
#                    else:
#                        ratingTable[i][j] = r.rating                
#                else:
#                    ratingTable[i][j] = 0
#            else:
#                ratingTable[i][j] = 0
#            j=j+1
#        i=i+1
#    return ratingTable, inFoldData, id2usr, id2bus
 

def get_folds(allRatings):
    folds = [[],[],[],[],[]]
    numRatings = len(allRatings)
    
    fld = []
    for i in range(0, numRatings):
        fld.append(i%5)
    random.shuffle(fld)
    
    
    for i in range(0, numRatings):
        ind = fld[i]
        folds[ind].append(allRatings.pop())
    return(folds)
    
def get_outfold_data(folds,thisFold):
    outFold = []
    for f in range(0,5):
        if f != thisFold:
            outFold = outFold + folds[f]
    return outFold

def run_nmf_mult_k(K):
    #loop over K
    resultFile = "/tmp/results.dat"
    fp = open(resultFile,"w")

    N = User.objects.count()
    M = Business.objects.count()
    fp.write("#NumUsers = "+str(N+1)+"\n")
    fp.write("#NumBusinesses = "+str(M+1)+"\n")
    allRatings = Rating.objects.all()
    fp.write("#NumRatings = "+str(allRatings.count())+"\n")
    allRatMatrix = []
    for r in allRatings:
        allRatMatrix.append([r.username.id-1, r.business.id-1, r.rating])
    folds = get_folds(allRatMatrix)
    for k in K:
        sumDist = 0
        for f in range(0,5): 
           # print("Running for fold "+str(f))
            outFold = get_outfold_data(folds, f)
            inFold = folds[f]
            nP, nQ = run_nmf_internal(outFold,N,M,k,fp=fp)
            # call matrix factorization
            dist = 0
            for r in inFold:
                uid = r[0] - 1
                bid = r[1] -1
                #print("Username " + str(r.username))
                #print("Business " + str(r.business.name))
                #print("Rating " + str(r.rating))
                prediction = numpy.dot(nP[uid],nQ[bid])
                #print("Prediction " + str(prediction))
                #print("")
                #print("")
                dist = dist + math.pow(abs(float(prediction) - float(r[2])),2)
            sumDist = sumDist + dist / len(inFold)
            print("For fold = "+str(f)+" dist = "+str(dist/len(inFold)))
        fp.write(str(k) + " " + str(sumDist/5)+ "\n")
        print("Average Distance for K= "+str(k) + " is " + str(sumDist/5))
        
        
  
# # http://www.albertauyeung.com/mf.php
#def matrix_factorization(R, P, Q, K, steps=2, alpha=0.0002, beta=0.02):
#    Q = Q.T
#    for step in xrange(steps):
#        print("Beginning step"+str(step))
#        for i in xrange(len(R)):
#            for j in xrange(len(R[i])):
#                if R[i][j] > 0:
#                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
#                    for k in xrange(K):
#                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
#                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
#                print("\t\tOne iteration of small-ass loop: "+str(j))
#            print("\tOne iteration of big-ass loop: "+str(i))
#        eR = numpy.dot(P,Q)
#        
#        e = 0
#        for i in xrange(len(R)):
#            for j in xrange(len(R[i])):
#                if R[i][j] > 0:
#                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
#                    for k in xrange(K):
#                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
#        if e < 0.001:
#            break
#    return P, Q.T



def matrix_factorization_new(allRatings,  P, Q, K, fp, steps=500, alpha=0.02, beta=0.02 ):
    Q = Q.T
    for step in xrange(steps):
        ct = 0
        for iter in range(0,len(allRatings)):
            r = allRatings[iter]
            uid = r.username.id -1
            bid = r.business.id -1
            eij = r.rating - numpy.dot(P[uid,:],Q[:,bid])
        
            for k in xrange(K):
                P[uid][k] = P[uid][k] + alpha * (2 * eij * Q[k][bid] - beta * P[uid][k])
                Q[k][bid] = Q[k][bid] + alpha * (2 * eij * P[uid][k] - beta * Q[k][bid])
            #if ct % 100 == 0:
            #    print(ct)
            ct = ct + 1
        #print("First loop done")
        #eR = numpy.dot(P,Q)
        e = 0
        for iter in range(0,len(allRatings)):
            r = allRatings[iter]
            uid = r.username.id -1
            bid = r.business.id -1
            e = e + pow(r.rating - numpy.dot(P[uid,:],Q[:,bid]), 2)
            for k in xrange(K):
                e = e + (beta/2) * (P[uid][k]*P[uid][k] + Q[k][bid]*Q[k][bid])
        
        fp.write(str(e))
        print(e)
        if e < 0.001:
            print("CONVERGED at:" + str(step))
            break
    print(str(e))
    return P, Q.T



def run_nmf_internal(R,N,M, K,fp):
   # P = numpy.random.rand(N,K)
    #Q = numpy.random.rand(M,K)
    
    P=[]
    Q=[]
    
    #run_nmf_c(list& ratings, int N, int M, int K, list& p_P, list &p_Q)
    
    fastnmf.run_nmf_c(R,N,M,K,P,Q)

  #  nP, nQ = matrix_factorization_new(R, P, Q, K,fp=fp)
    return P, Q
    #nR = numpy.dot(nP, nQ.T)

    #return nR
