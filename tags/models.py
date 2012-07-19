
from django.contrib.auth.models import User
from django.db import models
from ratings.models import Business
from wiki.models import Page


# Create your models here.

#for "hard" facts about the business (e.g. is it kosher?)
class HardTag(models.Model):
    creator = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    descr = models.TextField(max_length=1000)
    question = models.TextField(max_length=1000)
    
class BooleanQuestion(models.Model):
    hardtag = models.ForeignKey(HardTag)
    user = models.ForeignKey(User)
    business = models.ForeignKey('ratings.Business')
    date = models.DateTimeField(auto_now=True)
    agree = models.BooleanField() 

    




class Tag(models.Model):
    creator = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    descr = models.TextField(max_length=100)
    icon = models.TextField(max_length=100)

class CommentTag(models.Model):
    creator = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    comment=models.ForeignKey('comments.Comment')
    descr = models.TextField(max_length=1000)  


#User - Tag relationships
class UserTag(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag)
    
    
class BusinessTag(models.Model):
    business=models.ForeignKey('ratings.Business')
    creator = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag)
    

class TagRating(models.Model):
    tag = models.ForeignKey(BusinessTag)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    
