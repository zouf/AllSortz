from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.db import models
from wiki.models import Page



#decribes a listing   
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
        

class PageRelationship(models.Model):
    page = models.ForeignKey(Page)
    business = models.ForeignKey(Business)
    tag = models.ForeignKey('tags.Tag')
    
    
    
class Rating(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.username.username + " " + self.business.name + " " + str(self.rating)


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    business = models.ForeignKey(Business)
    reply_to = models.ForeignKey('self', related_name='replies', 
        null=True, blank=True)
    descr = models.TextField(max_length=2000)
    


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()