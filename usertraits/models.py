from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Trait(models.Model):
    date = models.DateTimeField(auto_now=True)
    descr = models.TextField(max_length=1000)
    creator = models.ForeignKey(User)
    name = models.TextField(max_length=200)
    
    
class TraitRelationship(models.Model):
    user = models.ForeignKey(User)
    trait = models.ForeignKey(Trait)
    relationship = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    