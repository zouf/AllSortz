from ratings.models import Business
from ratings.models import Rating
from ratings.models import Recommendation
from django.contrib.auth.models import User

from celery.execute import send_task

class RecEngine:
    best_recommendation_table = dict()   
    workerSpawned = False
    
    def setBestRecTable(self,newTable):
        print "Before"
        self.best_recommendation_table = newTable
        print self.best_recommendation_table
        print "After"
    
    def getBestRecTable(self):
        return self.best_recommendation_table
    
    def spawn_worker_task(self):
        if not self.workerSpawned:
            send_task("tasks.build_recommendations")
            self.workerSpawned = True
                
    # CALLED BY THE VIEW TO GET THE BES    T CURRENT RECOMMENDATION
    def get_best_current_recommendation(self, business, user):
      
            print(user)
            print(business)
            recset = Recommendation.objects.filter(username=user, business=business)
            print(recset[0])
            return recset[0].recommendation
         
    
        
