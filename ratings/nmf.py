
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

 
 # http://www.albertauyeung.com/mf.php
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
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


def run_nmf(R, K):
    N = len(R)
    M = len(R[0])

    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)
     
    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = numpy.dot(nP, nQ.T)

    return
    #matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):