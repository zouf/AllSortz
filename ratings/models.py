from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User

class Keyword(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Business(models.Model):
    name = models.CharField(max_length=50)
    
    average_rating = models.FloatField()

    lat = models.FloatField()
    lon = models.FloatField()
    
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField() # Yes, this is America-centric..
    
    keywords = models.ManyToManyField(Keyword, through='Grouping')

    def __unicode__(self):
        return self.name


class DontCare(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    

class Rating(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    def __unicode__(self):
        return self.username.username +  " " + self.business.name + " " + str(self.rating)




class Grouping(models.Model):
    business = models.ForeignKey(Business)
    keyword = models.ForeignKey(Keyword)



class Recommendation(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    recommendation = models.IntegerField()
    def __unicode__(self):
      return self.business.name

