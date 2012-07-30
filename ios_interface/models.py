from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
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

class Device(models.Model):
    os = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    deviceID = models.IntegerField()


class AllsortzUser(models.Model):
    user = models.OneToOneField(User)
    metric = models.BooleanField()
    device = models.ForeignKey(Device)

    def __unicode__(self):
        return self.user.username

class Discussion(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('self', related_name='replies', 
        null=True, blank=True)
    content = models.TextField(max_length=2000)

class CategoryDiscussion(Discussion):
    businesstag = models.ForeignKey('tags.BusinessTag')
  
class BusinessDiscussion(Discussion):
    business = models.ForeignKey('ratings.Business')

class PhotoDiscussion(Discussion):
    photo = models.ForeignKey('photos.BusinessPhoto')
