from celery.execute import send_task
from ratings.models import Rating, Business
from recommendation.models import UserFactor, BusinessFactor
from recommendation.normalization import getNormFactors
import numpy as np



class RecEngine:
    best_recommendation_table = dict()
    workerSpawned = False

    def setBestRecTable(self, newTable):
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

    def get_top_ratings(self, user,  numToPrint):
        NumFactors = 42
        ufset = UserFactor.objects.filter(user=user)
        myFactors = np.zeros(NumFactors)

        ratFilter = Rating.objects.filter(username=user)

        id2bus = {}
        ct = 0
        for bus in Business.objects.all():
            id2bus[ct] = bus
            ct = ct + 1

        busrelations = np.zeros((Business.objects.all().count(), NumFactors))
        for bc in id2bus.items():
            bfset = BusinessFactor.objects.filter(business=bc[1])
            for bf in bfset:
                busrelations[bc[0], bf.latentFactor] = bf.relation

        myFactors = np.zeros(NumFactors)
        for k in range(0, NumFactors):
            for r in ratFilter:
                bfset = BusinessFactor.objects.filter(business=r.business).filter(latentFactor=k)
                for bf in bfset:
                    relation = bf.relation
                    myFactors[k] += relation * r.rating

        myRatings = np.dot(myFactors, np.transpose(busrelations))

        dtype = [('index', int), ('rating', float)]

        pairedRatings = []
        for i in range(Business.objects.all().count()):
            pairedRatings.append((i, myRatings[i]))

        myPR = np.array(pairedRatings, dtype)

        print(myPR)
        myPR = np.sort(myPR, order=['rating'])
        print(myPR)

        top10 = []

        end = 0
        if len(myPR) < numToPrint:
            end = len(myPR)
        else:
            end = numToPrint
        for i in range(0, end):
            #dont append stuff user has already rated
            bus = id2bus[myPR[len(myPR) - i - 1]['index']]
            queryrat = Rating.objects.filter(username=user, business=bus)
            if queryrat.count() == 0:  # hasn't been a rating yet
                top10.append(id2bus[myPR[len(myPR) - i - 1]['index']])

        return top10

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
            myFactors[factor] = relation

        if ufset.count() == 0:
            return 0

        bfset = BusinessFactor.objects.filter(business=business)
        busFactors = np.zeros(NumFactors)
        for bf in bfset:
            factor = bf.latentFactor
            relation = bf.relation
            busFactors[factor] = relation

        if bfset.count() == 0:
            return 0

        prediction = np.dot(myFactors, busFactors) + getNormFactors(user.id, business.id)

        rec = round(prediction * 2) / 2  # round to half

        if rec > 5.0:
            rec = 5.0
        elif rec < 1.0:
            rec = 1.0

        #Recommendation.objects.filter(username=user, business=business)
        return rec
