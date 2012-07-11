from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.db import models

# Create your models he

#decribes a listing   
class Community(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    descr = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric..

    def __unicode__(self):
        return self.name
        
class UserMembership(models.Model):
    user = models.ForeignKey(User)
    logged_in = models.BooleanField()
    community = models.ForeignKey(Community)
    date = models.DateTimeField(auto_now=True)

        
class BusinessMembership(models.Model):
    business = models.ForeignKey('ratings.Business')
    community = models.ForeignKey(Community)
    date = models.DateTimeField(auto_now=True)

