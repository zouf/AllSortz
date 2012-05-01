# Create your views here.
from ratings.models import User
from ratings.models import Business
from ratings.models import Rating
from ratings.nmf import run_nmf_mult_k

def validate_production_data():
    K = [13,15,17]
    run_nmf_mult_k(K)
