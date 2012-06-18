from communities.models import Community
from django.contrib.auth.models import User
from django.db import models
from ratings.models import Business

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    descr = models.TextField(max_length=2000)
    creator = models.ForeignKey(User)
    number_of_items = models.PositiveIntegerField(help_text="How many items will be managed by this page?")
    date = models.DateTimeField(auto_now=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    community =models.ForeignKey(Community)


class ActivityWaypoint(models.Model):
    activity = models.ForeignKey(Activity)
    business = models.ForeignKey(Business)
    position = models.PositiveIntegerField()
    
    

class ActRating(models.Model):
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    