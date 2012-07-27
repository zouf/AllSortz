'''
Created on Jul 27, 2012

@author: zouf
'''
from ios_interface.models import Photo


#CODE NEEDS TO BE REFACTORED
def get_photo_url(b):
    qset  = Photo.objects.filter(business=b,is_default=True)
    if qset.count() < 1:
        return False
    ph = qset[0].image_thumb
    return ph.url


