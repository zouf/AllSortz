from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.db import models

    
class Business(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField(auto_now=True)

    lat = models.FloatField()
    lon = models.FloatField()

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric..

    def __unicode__(self):
        return self.name
        

class Rating(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.username.username + " " + self.business.name + " " + str(self.rating)




