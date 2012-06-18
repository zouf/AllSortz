from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from ratings.models import Business
import StringIO
import datetime

# Create your models here.


class BusinessPhoto(models.Model):

    user = models.ForeignKey(User)
    business = models.ForeignKey(Business)
    
    
    def image_upload_to_lg(self, filename):
        today = datetime.datetime.today()
        return 'user_uploads/%s/%s-%s-%s.%s.%s/large/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, filename)
          
    def image_upload_to_web(self, filename):
        today = datetime.datetime.today()
        return 'user_uploads/%s/%s-%s-%s.%s.%s/web/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, filename)

    def image_upload_to_thumb(self, filename):
        today = datetime.datetime.today()
        return 'user_uploads/%s/%s-%s-%s.%s.%s/thumb/%s' % (self.user.username, today.year, today.month, today.day, today.hour, today.minute, filename)

    
    image = models.ImageField(upload_to=image_upload_to_web)
    image_thumb = models.ImageField(upload_to=image_upload_to_thumb)
    image_large = models.ImageField(upload_to=image_upload_to_lg)
    
    
    title = models.CharField(blank=True, max_length=300)
    caption = models.TextField(blank=True)
    def save(self):
        #Original photo
        print(self.business.id)
        imgFile = Image.open(self.image)
        
        #Convert to RGB
        if imgFile.mode not in ('L', 'RGB'):
            imgFile = imgFile.convert('RGB')
        
        #Save a thumbnail for each of the given dimensions
        #The IMAGE_SIZES looks like:
        IMAGE_SIZES = { 'image'      : (300, 348),
                    'image_large'    : (600, 450),
                    'image_thumb'    : (200, 200) }

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
        super(BusinessPhoto, self).save()
    