from PIL import Image
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from os.path import basename
from ratings.models import Business
from tags.models import BusinessTag
import StringIO
import datetime

#from django.contrib.auth.models import User
#from ratings.models import Business
# Create your models here.





class  Photo(models.Model):
    user = models.ForeignKey(User) 
    business = models.ForeignKey(Business)   
    is_default = models.BooleanField()

    def image_upload_to_profile(self, filename):
        today = datetime.datetime.today()
        return 'user_uploads/profilepics/%s/%s-%s-%s.%s.%s/profile/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, basename(filename))
            
    def image_upload_to_thumb(self, filename):
        today = datetime.datetime.today()
        return 'user_uploads/%s/%s-%s-%s.%s.%s/web/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, basename(filename))
    
    def image_upload_to_medium(self, filename):
        today = datetime.datetime.today()
        return 'user_uploads/%s/%s-%s-%s.%s.%s/medium/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, basename(filename))
#    
#    def image_upload_to_mini(self,filename):
#        today = datetime.datetime.today()
#        return 'user_uploads/%s/%s-%s-%s.%s.%s/thumb2/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, filename)
#    
    image = models.ImageField(upload_to=image_upload_to_profile)
    image_medium = models.ImageField(upload_to=image_upload_to_medium)
    image_thumb = models.ImageField(upload_to=image_upload_to_thumb)

    #image_mini = models.ImageField(upload_to=image_upload_to_mini)

    date = models.DateTimeField(auto_now=True)
    
    
    title = models.CharField(blank=True, max_length=300)
    caption = models.TextField(blank=True)
    def save(self, isUpload):
        #Original photo
        
        if isUpload:
            imgFile = Image.open(self.image)
        else:
            imgFile = Image.open(str(self.image))
        #Convert to RGB
        print(imgFile)
        if imgFile.mode not in ('L', 'RGB'):
            imgFile = imgFile.convert('RGB')
        
        #Save a thumbnail for each of the given dimensions
        #The IMAGE_SIZES looks like:
        IMAGE_SIZES = {'image'    : (225, 225),
                       'image_medium'    : (125,125),
                       'image_thumb'    : (50,50)}

        #each of which corresponds to an ImageField of the same name
        for field_name, size in IMAGE_SIZES.iteritems():
            field = getattr(self, field_name)
            working = imgFile.copy()
            working.thumbnail(size, Image.ANTIALIAS)
            fp=StringIO.StringIO()
            working.save(fp, "png", quality=95)
            cf = ContentFile(fp.getvalue())
            field.save(name=self.image.name, content=cf, save=False);
        
        #Save instance of Photo
        super(Photo, self).save()
        
    
class PhotoRating(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField() 

#Describes a device that a user owns. Right now, the only type of device shouldbe iphones
class Device(models.Model):
    os = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    deviceID = models.IntegerField()

#A wrapper class for us that allows us to describe 
# important attributes associated with a user (devices, deals, preferences, etc.)
class AllsortzUser(models.Model):
    distance_threshold = models.IntegerField()
    user = models.OneToOneField(User)
    metric = models.BooleanField()
    device = models.ForeignKey(Device)

    def __unicode__(self):
        return self.user.username    
    
    
#base class of all deals / offers
class Offer(models.Model):
    business = models.ForeignKey(Business)
    description = models.CharField(max_length=1000)
    restricitons = models.CharField(max_length=1000)

    created_on = models.DateTimeField(auto_now=True)
    
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()  

#what the business is offering as a deal
class BusinessDeal(Offer):
    cost = models.IntegerField()
    number_allocated = models.IntegerField()
    number_used = models.IntegerField()
    
#What you can do to get something
class BusinessAction(Offer):
    reward_deal = models.ForeignKey(BusinessDeal)
    reward_value = models.IntegerField()
    number_allocated = models.IntegerField()
    number_used = models.IntegerField()

    
class ASUserDeal(models.Model):
    ASuser = models.ForeignKey(AllsortzUser)
    businessdeal = models.ForeignKey(BusinessDeal)
    #YYYY-MM-DD HH:MM
    received_on = models.DateTimeField() 
    used_on = models.DateTimeField() 

#A user action such as a check-in, or a purchase
class ASUserAction(models.Model):
    ASuser = models.ForeignKey(AllsortzUser)
    action = models.ForeignKey(BusinessAction)
    description = models.CharField(max_length=1000)
    location = models.PointField()
    
    #YYYY-MM-DD HH:MM
    completed_on = models.DateTimeField() 




#discussion-related items
class Discussion(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('self', related_name='replies', 
        null=True, blank=True)
    content = models.TextField(max_length=2000)

class DiscussionRating(models.Model):
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    rating = models.IntegerField()
    
    
    
    
    

class CategoryDiscussion(Discussion):
    businesstag = models.ForeignKey('tags.BusinessTag')
  
class BusinessDiscussion(Discussion):
    business = models.ForeignKey('ratings.Business')

class PhotoDiscussion(Discussion):
    photo = models.ForeignKey('photos.BusinessPhoto')
