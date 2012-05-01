"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from ratings.nmf import run_nmf_mult_k
from ratings.populate import generate_nmf_test, pop_test_user_bus_data

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
        K = [1,3,6,9,12]
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

