from django.contrib.auth.models import User
from django.db import models
from ratings.models import Business

# Create your models here.



class Tag(models.Model):
    creator = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    business=models.ForeignKey(Business)
    descr = models.TextField(max_length=1000)




class TagRating(models.Model):
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
