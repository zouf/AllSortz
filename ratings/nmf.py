import math
import random

import numpy
import sys
from django.conf import settings
from django.contrib.auth.models import User
from ratings.models import Business
from ratings.models import Rating
from data_import.views import user_rating_threshold
from data_import.views import bus_rating_threshold

import time

sys.path.append(settings.CLIB_DIR)
import fastnmf

OFFSET=-2

def get_folds(allRatings):
    folds = [[],[],[],[],[]]
    numRatings = len(allRatings)
    random.seed(666) 
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
    
    resultFile = settings.RESULTS_DIR+"u"+str(user_rating_threshold)+"_b"+str(bus_rating_threshold)+"_s"+str(Steps)+"_k"+str(K[0])+"-"+str(K[len(K)-1]);
    predictionFile = settings.RESULTS_DIR+"predictions_"+"u"+str(user_rating_threshold)+"_b"+str(bus_rating_threshold)+"_s"+str(Steps)+"_k"+str(K[0])+"-"+str(K[len(K)-1]);
    print(resultFile)
    fp = open(resultFile,"w")
    pred_fp = open(predictionFile, "w") 
    pred_fp.write("#K, f, Difference, Actual, Predicted");
    fp.write("#NumUsers = "+str(N+1)+'\n')
    fp.write("#NumBusinesses = "+str(M+1)+'\n')
    fp.write("#UserThresh = "+str(user_rating_threshold)+ '\n')
    fp.write("#BusinessThresh = "+str(bus_rating_threshold)+ '\n')
    fp.write("#NumRatings = "+str(allRatings.count())+'\n')
    fp.write("#Steps = " + str(Steps)+'\n')
    fp.write("#Alpha = " + str(Alpha)+'\n')
    fp.write("#TimeStart = "+str(time.asctime())+'\n')
    fp.write('#\n')
    fp.write('#K, AvgRSSRounded, AvgDistRounded, AvgRSSFloat, AvgDistFloat\n')
    fp.flush()
    allRatMatrix = []
    print("Moving data to an array...")
    for r in allRatings:
<<<<<<< HEAD
<<<<<<< HEAD
        allRatMatrix.append([r.username.id-1, r.business.id-1, r.rating] + OFFSET)
=======
        allRatMatrix.append([r.username.id-1, r.business.id-1, (r.rating + OFFSET)])
>>>>>>> ff0597e87bde90e78c9842c41db8183581411643
=======
        allRatMatrix.append([r.username.id-1, r.business.id-1, (r.rating + OFFSET)])
>>>>>>> ff0597e87bde90e78c9842c41db8183581411643
    print("Generating Folds...");
    folds = get_folds(allRatMatrix)
    print("Fold Generation Complete...")
    for k in K:
        print("Running on K="+str(k)+" Starting at time= "+ time.asctime())
        sumDistRounded = 0
        sumRSSRounded = 0
        sumDistFloat = 0.0
        sumRSSFloat = 0.0
        ctr = 0
        for f in range(0,5):    
            outFold = get_outfold_data(folds, f)
            inFold = folds[f]
            time_before = time.clock()
            nP, nQ = run_nmf_internal(outFold,N,M,k, Steps, Alpha, fp=fp)
            elapsed = time.clock() - time_before;
            print("\tK="+str(k)+" Fold=" +str(f)+" TimeElapsed="+ str(elapsed/60) + " minutes")
            
            #for keeping track of rss, average distance for floats and rounded
            distFloat = 0.0
            rssFloat = 0.0
            rssRounded = 0
            distRounded = 0
            inFoldLen = len(inFold)
            for r in inFold:
                uid = r[0] - 1
                bid = r[1] - 1
<<<<<<< HEAD
                
=======

<<<<<<< HEAD
>>>>>>> ff0597e87bde90e78c9842c41db8183581411643
=======
>>>>>>> ff0597e87bde90e78c9842c41db8183581411643
                r[2] = r[2] - OFFSET
                prediction = numpy.dot(nP[uid],nQ[bid]) - OFFSET
                
                roundR = round(r[2])
                roundP = round(prediction)
                
                floatR = float(r[2])
                floatP = float(prediction)
                if r[2] > 5:
                    floatR = 5.0
                    roundR = 5;
                elif r[2] < 1:
                    roundR = 1;
                    floatR = 1.0
                    
                if prediction > 5:
                    roundP = 5
                    floatP = 5.0
                elif prediction < 1:
                    roundP = 1
                    floatP = 1.0


                #print("Username " + str(r.username))
                #print("Business " + str(r.business.name))
                #print("Rating " + str(r.rating))
                #print("Prediction " + str(prediction))
                      
                rssFloat +=    math.pow(abs(floatP - floatR),2)
                distFloat +=   abs(floatP - floatR)
                rssRounded +=  math.pow(abs(roundP - roundR),2)
                distRounded += abs(roundP - roundR)
                #pred_fp.write(str(abs(floatP - floatR)) + ", " + str(floatR) + ", " + str(floatP) + ", " +str(k) + ", " + str(f) +  '\n');
                pred_fp.write(str(abs(floatP-floatR)) + " " + str(floatR) + " " + str(floatP) + " " + '\n');
                if ctr % 1000 == 0:
                  pred_fp.flush()
                ctr += 1
            sumDistRounded +=  distRounded / inFoldLen
            sumRSSRounded += rssRounded/ inFoldLen
            sumDistFloat +=  distFloat / inFoldLen
            sumRSSFloat +=  rssFloat/ inFoldLen
            print("\t\t RSS_float="  + str(rssFloat/inFoldLen)   + " Distance_float=" + str(distFloat/inFoldLen))
            print("\t\t RSS_rounded="+ str(rssRounded/inFoldLen) + " Distance_rounded=" + str(distRounded/inFoldLen))
        result_1 = str(sumRSSRounded/5)+ ", " + str(sumDistRounded/5) 
        result_2 = str(sumRSSFloat/5)+ ", " + str(sumDistFloat/5) 
        fp.write(str(k) + ", " + result_1 + ", " + result_2 + '\n')
        fp.flush()
        print("K="+str(k) + "Rounded: " + result_1 + " Float: " + result_2)
        
    fp.write("#TimeEnd = "+str(time.asctime())+'\n')
    pred_fp.flush()
    fp.flush()
    fp.close()
    pred_fp.close()
  


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
