from celery.execute import send_task
from django.contrib.auth.models import User
from ratings.models import Business, Rating, Recommendation, UserFactor, \
    BusinessFactor
from ratings.normalization import getBusAvg, getNormFactors
import numpy as np

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
      
        #  my.factors <- me %*% m@fit@W
        #  barplot(my.factors)
        #  my.prediction <- my.factors %*% t(m@fit@W)
        #  items$title[order(my.prediction, decreasing=T)[1:10]]
        
        NumFactors = 42
        ufset = UserFactor.objects.filter(user=user)
        myFactors = np.zeros(NumFactors)
    
        for uf in ufset:
            factor = uf.latentFactor
            relation = uf.relation
            myFactors[factor]=relation
        
        if uf.count() == 0:
          return 0


        bfset = BusinessFactor.objects.filter(business=business)       
        busFactors = np.zeros(NumFactors)
        for bf in bfset:
            factor = bf.latentFactor
            relation = bf.relation
            busFactors[factor]=relation
        
        if bf.count() == 0:
          return 1
        
        prediction = np.dot(myFactors,busFactors) +  getNormFactors(user.id, business.id)
        
        rec = round(prediction*2)/2 #round to half
        
        if rec > 5.0:
            rec = 5.0
        elif rec < 1.0:
            rec = 1.0 
            
        #Recommendation.objects.filter(username=user, business=business)
        return rec
     

        
