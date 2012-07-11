from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.db import models
from wiki.models import Page
from django.contrib.gis.db import models as gismodels



#decribes a listing   
class Business(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    lat = models.FloatField()
    lon = models.FloatField()

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric..

    def __unicode__(self):
        return self.name


     
class UserFavorite(models.Model):
    business= models.ForeignKey(Business)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
     
        
#decribes a listing   
class Community(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    descr = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric..

    def __unicode__(self):
        return self.name
        

class FacebookUser(models.Model):
    fbuser_id = models.IntegerField()
    user = models.ForeignKey(User)


class PageRelationship(models.Model):
    page = models.ForeignKey(Page)
    business = models.ForeignKey(Business)
    tag = models.ForeignKey('tags.Tag')
    
    
    
class Rating(models.Model):
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.user) + " " + str(self.business.name) + " " + str(self.rating)


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('self', related_name='replies', 
        null=True, blank=True)
    descr = models.TextField(max_length=2000)
    
# Create your models here.
class TagComment(models.Model):
    thread = models.ForeignKey(Comment)
    tag = models.ForeignKey('tags.Tag')
    business = models.ForeignKey(Business)
    date = models.DateTimeField(auto_now=True)
  

class BusinessComment(models.Model):
    business = models.ForeignKey(Business)
    thread = models.ForeignKey(Comment)
    date = models.DateTimeField(auto_now=True)


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()