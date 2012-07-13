# Create your views here.
from django.contrib.auth.models import User
from django.db import models


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
    business = models.ForeignKey('ratings.Business')
    date = models.DateTimeField(auto_now=True)
  

class BusinessComment(models.Model):
    business = models.ForeignKey('ratings.Business')
    thread = models.ForeignKey(Comment)
    date = models.DateTimeField(auto_now=True)

class PhotoComment(models.Model):
    photo = models.ForeignKey('photos.BusinessPhoto')
    thread = models.ForeignKey(Comment)
    date = models.DateTimeField(auto_now=True)
