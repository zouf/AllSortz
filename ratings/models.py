from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User


class Keyword(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=250)

    average_rating = models.FloatField()

    lat = models.FloatField()
    lon = models.FloatField()

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric..

    keywords = models.ManyToManyField(Keyword, through='Grouping')

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.username.username + " " + self.business.name + " " + str(self.rating)


class Tip(models.Model):
    user = models.ForeignKey(User)
    business = models.ForeignKey(Business)
    descr = models.TextField(max_length=2000)


class Review(models.Model):
    user = models.ForeignKey(User)
    business = models.ForeignKey(Business)
    descr = models.TextField(max_length=2000)


class ReviewRating(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.username.username + " " + self.business.name + " " + str(self.rating)


class TipRating(models.Model):
    tip = models.ForeignKey(Tip)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.username.username + " " + self.business.name + " " + str(self.rating)


class Grouping(models.Model):
    business = models.ForeignKey(Business)
    keyword = models.ForeignKey(Keyword)
