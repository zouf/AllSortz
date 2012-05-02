# Create your views here.
from data_import.views import read_dataset
from ratings.nmf import run_nmf_mult_k
from ratings.populate import pop_test_user_bus_data, generate_nmf_test


def validate_production_data():

    #read_dataset()
    # K = [12,13,14,15,16,17,18]
    K = [18,20,22,24,26,28,30]
    Steps = 20000
    Alpha = 0.0035
    run_nmf_mult_k(K,Steps,Alpha)

def simple_validate():
    pop_test_user_bus_data(numUsers=30, numBusinesses=20)
    generate_nmf_test(numFactors=6, density=.3)
    print("here?")
    K = [1,3,6,9,12]
    Steps = 20000
    Alpha = 0.0035
    run_nmf_mult_k(K,Steps,Alpha)