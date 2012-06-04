from PIL import Image
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.core.files.base import ContentFile, File
from django.db import models
import StringIO
import datetime


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
    
    

class Rating(models.Model):
    business = models.ForeignKey(Business)
    username = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.username.username + " " + self.business.name + " " + str(self.rating)



class Tag(models.Model):
    creator = models.ForeignKey(User)
    business=models.ForeignKey(Business)
    descr = models.TextField(max_length=1000)


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


class TipRating(models.Model):
    tip = models.ForeignKey(Tip)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()


class TagRating(models.Model):
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey(User)
    rating = models.PositiveSmallIntegerField()


class Grouping(models.Model):
    business = models.ForeignKey(Business)
    keyword = models.ForeignKey(Keyword)
