# Create your views here.
from ratings.models import Business, Rating, User
from ratings.nmf import run_nmf_mult_k
from ratings.populate import pop_test_user_bus_data, generate_nmf_test
from data_import.views import read_dataset
import sys


def validate_production_data():

    read_dataset()
   # K = [12,13,14,15,16,17,18]
    K = [22,24]
    run_nmf_mult_k(K)

def simple_validate():
    pop_test_user_bus_data(numUsers=30, numBusinesses=20)
    generate_nmf_test(numFactors=6, density=.3)
    K = [1,3,6,9,12]
    run_nmf_mult_k(K)