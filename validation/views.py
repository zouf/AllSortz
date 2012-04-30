# Create your views here.
from ratings.nmf import get_rating_folds

def run_nmf(request):
    print("In run_nmf")
    get_rating_folds()