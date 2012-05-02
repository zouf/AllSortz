import math
import random

import numpy
import sys
from django.conf import settings
from django.contrib.auth.models import User
from ratings.models import Business
from ratings.models import Rating

import time

sys.path.append(settings.CLIB_DIR)
import fastnmf

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

def get_p_q_best(k, steps, alpha):
    N = User.objects.count()
    M = Business.objects.count()
    print("Get ratings from DB")
    allRatings = Rating.objects.all()
    print("Moving data to an array...")
    allRatMatrix = []
    for r in allRatings:
        allRatMatrix.append([r.username.id-1, r.business.id-1, r.rating])
    nP, nQ = run_nmf_internal(allRatMatrix,N,M,k,steps,alpha,0)
    return nP, nQ


def run_nmf_mult_k(K,Steps,Alpha):
    N = User.objects.count()
    M = Business.objects.count()
    allRatings = Rating.objects.all()
    
    resultFile = settings.RESULTS_DIR+"u"+str(N+1)+"_b"+str(M+1)+"_s"+str(Steps)+"_k"+str(K[0])+"-"+str(K[len(K)-1]);
    print(resultFile)
    fp = open(resultFile,"w")
    fp.write("#NumUsers = "+str(N+1)+'\n')
    fp.write("#NumBusinesses = "+str(M+1)+'\n')
    fp.write("#NumRatings = "+str(allRatings.count())+'\n')
    fp.write("#Steps = " + str(Steps)+'\n')
    fp.write("#Alpha = " + str(Alpha)+'\n')
    fp.write("#Time = "+str(time.asctime())+'\n')
    fp.write('#\n')
    fp.write('#K, AvgRSS, AvgDist\n')
    allRatMatrix = []
    print("Moving data to an array...")
    for r in allRatings:
        allRatMatrix.append([r.username.id-1, r.business.id-1, r.rating])
    print("Generating Folds...");
    folds = get_folds(allRatMatrix)
    print("Fold Generation Complete...")
    for k in K:
        sumDist = 0
        sumRSS = 0
        for f in range(0,5):    
            # print("Running for fold "+str(f))
            outFold = get_outfold_data(folds, f)
            inFold = folds[f]
            nP, nQ = run_nmf_internal(outFold,N,M,k, Steps, Alpha, fp=fp)
            # call matrix factorization
            dist = 0
            rss = 0
            for r in inFold:
                uid = r[0] - 1
                bid = r[1] -1
                #print("Username " + str(r.username))
                #print("Business " + str(r.business.name))
                #print("Rating " + str(r.rating))
                prediction = numpy.dot(nP[uid],nQ[bid])
                
                roundR = round(r[2])
                roundP = round(prediction)
                if r[2] > 5:
                    roundR = 5.0;
                elif r[2] < 1:
                    roundR = 1.0
                    
                if prediction > 5:
                    roundP = 5.0
                elif prediction < 1:
                    roundP = 1.0
                    
                
                
                #print("Prediction " + str(prediction))
                #print("")
                #print("")
                rss = rss + math.pow(abs(roundP - roundR),2)
                dist = dist + abs(roundP - roundR)

            sumDist = sumDist + dist / len(inFold)
            sumRSS = sumRSS + rss/ len(inFold)
            print("For fold = "+str(f)+" rss = "+str(rss/len(inFold)) + " dist = " + str(dist/len(inFold)))
        fp.write(str(k) + ", " + str(sumRSS/5)+ " , " + str(sumDist/5) + '\n')
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


#
#def matrix_factorization_new(allRatings,  P, Q, K, fp, steps=500, alpha=0.02, beta=0.02 ):
#    Q = Q.T
#    for step in xrange(steps):
#        ct = 0
#        for iter in range(0,len(allRatings)):
#            r = allRatings[iter]
#            uid = r.username.id -1
#            bid = r.business.id -1
#            eij = r.rating - numpy.dot(P[uid,:],Q[:,bid])
#        
#            for k in xrange(K):
#                P[uid][k] = P[uid][k] + alpha * (2 * eij * Q[k][bid] - beta * P[uid][k])
#                Q[k][bid] = Q[k][bid] + alpha * (2 * eij * P[uid][k] - beta * Q[k][bid])
#            #if ct % 100 == 0:
#            #    print(ct)
#            ct = ct + 1
#        #print("First loop done")
#        #eR = numpy.dot(P,Q)
#        e = 0
#        for iter in range(0,len(allRatings)):
#            r = allRatings[iter]
#            uid = r.username.id -1
#            bid = r.business.id -1
#            e = e + pow(r.rating - numpy.dot(P[uid,:],Q[:,bid]), 2)
#            for k in xrange(K):
#                e = e + (beta/2) * (P[uid][k]*P[uid][k] + Q[k][bid]*Q[k][bid])
#        
#        fp.write(str(e))
#        print(e)
#        if e < 0.001:
#            print("CONVERGED at:" + str(step))
#            break
#    print(str(e))
#    return P, Q.T



def run_nmf_internal(R,N,M, K, Steps, Alpha, fp):
    # P = numpy.random.rand(N,K)
    #Q = numpy.random.rand(M,K)    
    P=[]
    Q=[]    
    #run_nmf_c(list& ratings, int N, int M, int K, int p_Steps, double p_Alpha, list& p_P, list &p_Q)
    fastnmf.run_nmf_from_python(R,N,M,K, Steps, Alpha, P,Q)
    return P, Q
    #nR = numpy.dot(nP, nQ.T)
    #return nR
