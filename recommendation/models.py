from django.contrib.auth.models import User
from django.db import models
from ratings.models import Business

# Create your models here.


class Recommendation(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    recommendation = models.IntegerField()

    def __unicode__(self):
        return self.business.name


class BusinessFactor(models.Model):
    business = models.ForeignKey(Business)
    latentFactor = models.IntegerField()
    relation = models.FloatField()


class UserFactor(models.Model):
    user = models.ForeignKey(User)
    latentFactor = models.IntegerField()
    relation = models.FloatField()
