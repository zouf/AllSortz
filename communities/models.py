from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USStateField
from django.db import models
from ratings.models import Business

# Create your models here.


class Community(models.Model):
    name = models.CharField(max_length=250)
    descr = models.TextField()
    date = models.DateField(auto_now=True)

    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric..

    def __unicode__(self):
        return self.name
        
        
class UserMembership(models.Model):
    user = models.ForeignKey(User)
    logged_in = models.BooleanField()
    community = models.ForeignKey(Community)
    date = models.DateField(auto_now=True)

        
class BusinessMembership(models.Model):
    business = models.ForeignKey(Business)
    community = models.ForeignKey(Community)
    date = models.DateField(auto_now=True)
