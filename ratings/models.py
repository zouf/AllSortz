from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.db import models
from django.utils.encoding import smart_str
from wiki.models import Page
import simplejson
import urllib
import urllib2



#decribes a listing   
class Business(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    lat = models.FloatField()
    lon = models.FloatField()

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = USStateField()  # Yes, this is America-centric.
    

    def __unicode__(self):
        return self.name
    def save(self):
        loc = self.address + " " + self.city + ", " + self.state
        location = urllib.quote_plus(smart_str(loc))
        dd = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % location).read() 
        ft = simplejson.loads(dd)
        if ft["status"] == 'OK':
            lat = str(ft["results"][0]['geometry']['location']['lat']) 
            lng = str(ft["results"][0]['geometry']['location']['lng'])
        latlng = [lat, lng]
        self.lat = latlng[0]
        self.lon = latlng[1]
        super(Business, self).save()




     
class UserFavorite(models.Model):
    business= models.ForeignKey(Business)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
        

class FacebookUser(models.Model):
    fbuser_id = models.IntegerField()
    user = models.ForeignKey(User)


class PageRelationship(models.Model):
    page = models.ForeignKey(Page)
    businesstag = models.ForeignKey('tags.BusinessTag')


class CommentRating(models.Model):
    comment = models.ForeignKey('comments.Comment')
    user = models.ForeignKey(User)

    
    
    
    
class Rating(models.Model):
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.user) + " " + str(self.business.name) + " " + str(self.rating)


