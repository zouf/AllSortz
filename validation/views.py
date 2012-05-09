# Create your views here.
from data_import.views import read_dataset
from django.conf import settings
from django.db import transaction
from ratings.models import Business, Recommendation, User
from ratings.nmf import run_nmf_mult_k, get_p_q_best
from ratings.populate import pop_test_user_bus_data, generate_nmf_test
import numpy

def build_pred_server():
    k=30
    Steps = 1000
    Alpha = 0.004
    P, Q = get_p_q_best(k, Steps, Alpha)
    Predictions = numpy.dot(P,numpy.transpose(Q))
    i = 1
    predictions = []
    for row in Predictions:
        print(len(row))
        j = 1
        bus = Business.objects.get(id=j)
        for cell in row:
            usr = User.objects.get(id=i)
            p = Recommendation(business=bus,recommendation=cell,username=usr)
            predictions.append(p)
            j+=1
        i+=1
    Recommendation.objects.bulk_create(predictions)
    transaction.commit();
    

def find_categories_best_k(k):
    Steps = 1000
    Alpha = 0.004
    P, Q = get_p_q_best(k, Steps, Alpha)
    zipQ = zip(*Q)
    latentNum = 0
    for l in zipQ: #{
      maxVal = max(l)
      cutOff = 0.8 * maxVal
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


def init():
  read_dataset()
  
def val_nmf(K,Steps,Alpha):
  run_nmf_mult_k(K,Steps,Alpha)

def nmf_specific_k(k,Steps):
  K=[k]
  read_dataset()
  Alpha = 0.004
  run_nmf_mult_k(K,Steps,Alpha)


def validate_production_data():
    # K = [12,13,14,15,16,17,18]
#    K = [12,14,16,18,20,22,24,26]
    #K = [2,5,10,15,20,25,30,35,40]
    K = [30]
    #Steps = 30000
    Steps = 1000
    Alpha = 0.0003
    run_nmf_mult_k(K,Steps,Alpha)

def simple_validate():
    pop_test_user_bus_data(numUsers=30, numBusinesses=20)
    generate_nmf_test(numFactors=6, density=.3)
    print("here?")
    K = [1,3,6,9,12]
    Steps = 20000
    Alpha = 0.0004
    run_nmf_mult_k(K,Steps,Alpha)
