from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.db import models
from wiki.models import Page

import coords

#decribes a listing   
class Business(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    coords = coords.CoordsField()

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric.
    

    def __unicode__(self):
        return self.name




     
class UserFavorite(models.Model):
    business= models.ForeignKey(Business)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
        

class FacebookUser(models.Model):
    fbuser_id = models.IntegerField()
    user = models.ForeignKey(User)


class PageRelationship(models.Model):
    page = models.ForeignKey(Page)
    business = models.ForeignKey(Business)
    tag = models.ForeignKey('tags.Tag')


class CommentRating(models.Model):
    comment = models.ForeignKey('comments.Comment')
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField() 
    
    
    
    
    
class Rating(models.Model):
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.user) + " " + str(self.business.name) + " " + str(self.rating)


