"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from numpy.core.numeric import dot
from ratings.models import Business, Rating
from ratings.nmf import run_nmf_mult_k
from ratings.populate import create_user, create_business
import random

#


def createusers(n):
    for i in range(1, n + 1):
        u = create_user("tst" + str(i))
        u.id = i
        u.save()


def createbusinesses(n):
    for i in range(1, n + 1):
        b = create_business('b' + str(i), "tst", "NY", "tst", 0, 0)
        b.id = i
        b.save()


def generate_nmf_test(numFactors, density):
    allUsers = User.objects.all()
    allBusinsses = Business.objects.all()
    random.seed(666)
    newP = []
    for u in range(0, allUsers.count()):
        if u not in newP:
            newP.append([])
        for k in range(0, numFactors):
            rif = random.uniform(0, 1)
            newP[u].append(rif)

    newQ = []
    for k in range(0, numFactors):
        newQ.append([])
        for j in range(0, allBusinsses.count()):
            rif = random.uniform(0, 1)
            newQ[k].append(rif)

    initR = dot(newP, newQ)

    i = 0
    for u in allUsers:
        j = 0
        for b in allBusinsses:
            chance = random.uniform(0, 1)
            if(chance < density):
                rat = Rating(business=b, username=u, rating=float(initR[i][j]))
                rat.save()
            j = j + 1
    i = i + 1


def pop_test_user_bus_data(numUsers, numBusinesses):
    Rating.objects.all().delete()
    #User.objects.exclude(username="joey").exclude(username="zouf").delete()
    User.objects.all().delete()
    Business.objects.all().delete()
    createbusinesses(numBusinesses)
    createusers(numUsers)
    return


def populate_test_data(numUsers, numBusinesses):
    Rating.objects.all().delete()
    User.objects.all().delete()
    Business.objects.all().delete()
    createbusinesses(numBusinesses)
    createusers(numUsers)
    #generateTest()
    return


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TestNMF(TestCase):
    def test_gen_model(self):
        pop_test_user_bus_data(numUsers=30, numBusinesses=20)
        generate_nmf_test(numFactors=6, density=.3)
        K = [1, 3, 6, 9, 12]
        run_nmf_mult_k(K)


#    def test_bin_nmf(self):
#        R = [
#             [2,1,0,2],
#             [1,0,2,1],
#             [2,1,0,2],
#             [2,0,0,1],
#             [0,1,2,2],
#            ]
#
#        R = numpy.array(R)
#
#        N = len(R)
#        M = len(R[0])
#        K = 2
#
#        P = numpy.random.rand(N,K)
#        Q = numpy.random.rand(M,K)
#
#        nP, nQ = matrix_factorization(R, P, Q, K)
#        nR = numpy.dot(nP, nQ.T)
#        print(nR)
#        return
#
#
#    def test_basic_nmf(self):
#        R = [
#             [5,3,0,1],
#             [4,0,0,1],
#             [1,1,0,5],
#             [1,0,0,4],
#             [0,1,5,4],
#            ]
#
#        R = numpy.array(R)
#
#        N = len(R)
#        M = len(R[0])
#        K = 2
#        print("two latent variables")
#        P = numpy.random.rand(N,K)
#        Q = numpy.random.rand(M,K)
#
#        nP, nQ = matrix_factorization(R, P, Q, K)
#        nR = numpy.dot(nP, nQ.T)
#        print(nR)
#        return
#
#    def test_disjoint_nmf(self):
#        R = [
#             [0,2,2],
#             [2,2,0]
#            ]
#
#        R = numpy.array(R)
#
#        N = len(R)
#        M = len(R[0])
#        K = 1
#
#        P = [ [1],
#              [1]
#            ]
#
#        P = numpy.array(P)
#
#        Q = [ [1],
#              [1]
#            ]
#
#        Q = numpy.array(Q)
#    #    P = numpy.random.rand(N,K)
#     #   Q = numpy.random.rand(M,K)
#
#        print(P)
#        print(Q)
#        nP, nQ = matrix_factorization(R, P, Q, K)
#        nR = numpy.dot(nP, nQ.T)
#        print(nP)
#        print(nQ)
#        print(nR)
