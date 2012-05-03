# Create your views here.
from data_import.views import read_dataset
from django.conf import settings
from ratings.nmf import run_nmf_mult_k,get_p_q_best
from ratings.populate import pop_test_user_bus_data, generate_nmf_test
from ratings.models import Business

Steps = 200
Alpha = 0.0035

def find_categories_best_k(k):
    P, Q = get_p_q_best(k, Steps, Alpha)
    zipQ = zip(*Q)
    latentNum = 0
    for l in zipQ: #{
      maxVal = max(l)
      cutOff = 0.5 * maxVal
      print "  Cutoff is: " + str(cutOff)

      relevantBus = []
      for i in xrange(0, len(l)):
        if l[i] > cutOff:
          # this business is relevant to this latent variable
          # save the id (index is id-1) to use in db look up later
          relevantBus.append(i+1) 
      
      print "    " + str(len(relevantBus)) + " businesses past cutoff"
      # For this latent variable, we now have all businesses IDs,
      # print out all of the labels associated with these businesses
      fp = open(settings.RESULTS_DIR + "latent_" + str(latentNum), 'w')
      buses = Business.objects.filter(pk__in=relevantBus)
      for b in buses:
        keywords = b.keywords.all()
        print "      " + str(len(keywords)) + " keywords for business"
        for k in keywords:
          fp.write(str(k) + "\n")
        fp.write("\n")

      fp.close()
      latentNum = latentNum + 1
    #}

         


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
