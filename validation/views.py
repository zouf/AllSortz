# Create your views here.
from data_import.views import read_dataset
from ratings.nmf import run_nmf_mult_k,get_p_q_best
from ratings.populate import pop_test_user_bus_data, generate_nmf_test

Steps = 20000
Alpha = 0.0035

def find_categories_best_k(k):
    P, Q = get_p_q_best(k, Steps, Alpha)
    zipQ = zip(*Q)
    for l in zipQ:
      maxVal = max(l)
      cutOff = 0.9 * maxVal
      print "Cutoff is: " + str(cutOff)

      relevantBus = []
      for i in range(0, len(l)):
        if l[i] > cutOff:
          # this business is relevant to this latent variable
          # save the id (index is id-1) to use in db look up later
          relevantBus.append(i+1) 
      
      # For this latent variable, we now have all businesses IDs,
      # print out all of the labels associated with these businesses


         


def validate_production_data():

    #read_dataset()
    # K = [12,13,14,15,16,17,18]
    K = [18,20,22,24,26,28,30]
    run_nmf_mult_k(K,Steps,Alpha)

def simple_validate():
    pop_test_user_bus_data(numUsers=30, numBusinesses=20)
    generate_nmf_test(numFactors=6, density=.3)
    print("here?")
    K = [1,3,6,9,12]
    run_nmf_mult_k(K,Steps,Alpha)
