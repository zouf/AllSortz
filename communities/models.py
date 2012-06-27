from django.contrib.auth.models import User
from django.db import models
from ratings.models import Community

# Create your models he


        
class UserMembership(models.Model):
    user = models.ForeignKey(User)
    logged_in = models.BooleanField()
    community = models.ForeignKey(Community)
    date = models.DateTimeField(auto_now=True)

        
class BusinessMembership(models.Model):
    business = models.ForeignKey('ratings.Business')
    community = models.ForeignKey(Community)
    date = models.DateTimeField(auto_now=True)

