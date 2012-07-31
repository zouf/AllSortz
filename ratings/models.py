from django.contrib.auth.models import User, UserManager
from django.contrib.gis.db import models
from django.contrib.gis.geos.factory import fromstr
from django.contrib.localflavor.us.forms import USPhoneNumberField, \
    USZipCodeField
from django.contrib.localflavor.us.models import USStateField
from django.utils.encoding import smart_str
from geopy import geocoders, distance
from wiki.models import Page
import simplejson
import urllib
import urllib2


#class RatingManager(models.Manager):
#    def get_query_set(self):
#        allBusinesses = super(Business, self).get_query_set().all()
#        for b in allBusinesses:      
#            #b.average_rating =  round(getBusAvg(b.id) * 2) / 2
#            #b.photo = get_photo_url(b)
#            #b.numberOfRatings = getNumRatings(b.id)
#            #b.numberOfLoves = getNumLoved(b)
#            #b.numberOfLikes = getNumLiked(b)
#            bustags = BusinessTag.objects.filter(business=b).exclude(tag=get_master_summary_tag())
#            b.tags = []
#            for bt in bustags:
#                if not is_master_summary_tag(bt):
#                    b.tags.append(bt)
#        return allBusinesses


class Business(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    lat = models.FloatField()
    lon = models.FloatField()
    geom = models.PointField()

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    

    # Right now: America centric 
    state = USStateField()  
    phone = USPhoneNumberField()
    zipcode = USZipCodeField()
    
    objects = models.GeoManager()
    def __unicode__(self):
        return self.name
    
    #gets distance between this business and a user
    def get_distance(self,user):
        if user.current_location:
            distance.distance(user.current_location,(self.lat,self.lon)).miles
        else:
            return None
        
    def save(self):
        loc = self.address + " " + self.city + ", " + self.state        
        location = urllib.quote_plus(smart_str(loc))
        dd = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % location).read() 
        ft = simplejson.loads(dd)
        if ft["status"] == 'OK':
            lat = str(ft["results"][0]['geometry']['location']['lat']) 
            lng = str(ft["results"][0]['geometry']['location']['lng'])
            zipcode = None
            for jsonStr in ft["results"][0]['address_components']:
                print jsonStr
                if 'types' in jsonStr:
                    for tp in jsonStr['types']:
                        if tp == " postal_code":
                            zipcode = str.long_name
                            break
            
        print('trying to save!') 
        self.zipcode  = zipcode
        self.lat = lat
        self.lon = lng 
        self.geom = fromstr('POINT('+str(self.lon)+ ' '+str(self.lat)+')', srid=4326)
        
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
    rating = models.IntegerField()

    
    
    
    
class Rating(models.Model):
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.user) + " " + str(self.business.name) + " " + str(self.rating)




