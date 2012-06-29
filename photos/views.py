# Create your views here.
#for businesses


#gets thumb photo (small)
from photos.models import BusinessPhoto
def get_photo_thumb_url(b):
    qset  = BusinessPhoto.objects.filter(business=b)
    if qset.count() < 1:
        return False
    ph = qset[0].image_thumb
    return ph.url


#gets web photo (medium)
def get_photo_web_url(b):
    qset  = BusinessPhoto.objects.filter(business=b)
    if qset.count() < 1:
        return None
    ph = qset[0].image
    return ph.url


#gets web photo (large)
def get_photo_large_url(b):
    qset  = BusinessPhoto.objects.filter(business=b)
    if qset.count() < 1:
        return False
    ph = qset[0].image_large
    return ph.url

#gets web photo (large)
def get_photo_mini_url(b):
    qset  = BusinessPhoto.objects.filter(business=b)
    if qset.count() < 1:
        return False
    ph = qset[0].image_mini
    return ph.url
