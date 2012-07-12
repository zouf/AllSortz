# Create your views here.
#for businesses


#gets thumb photo (small)
from communities.models import Community
from communities.views import get_community
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.context import RequestContext
from photos.models import BusinessPhoto
from rateout import settings
from ratings.models import Business
from tags.models import Tag, HardTag
from tags.views import get_tags_user, get_top_tags, get_all_sorts
from urllib import urlretrieve
import logging
import sys


logger = logging.getLogger(__name__)

def get_gallery_context(user):
    user_tags = get_tags_user(user,"")
    top_tags = get_top_tags(10)    
    community = get_community(user)

    context = {\
            'communities': Community.objects.all(),\
            'community': community,\
              'user_sorts':user_tags,\
            'top_sorts':top_tags,\
             'tags': Tag.objects.all(),\
             'questions': HardTag.objects.all(),\
            'all_sorts':get_all_sorts(4),\
            'location_term':community }   
    return context    


def get_photo_thumb_url(b):
    qset  = BusinessPhoto.objects.filter(business=b,is_default=True)
    if qset.count() < 1:
        return False
    ph = qset[0].image_thumb
    return ph.url


#gets web photo (medium)
def get_photo_web_url(b):
    qset  = BusinessPhoto.objects.filter(business=b,is_default=True)
    if qset.count() < 1:
        return None
    ph = qset[0].image
    return ph.url


#gets web photo (large)
def get_photo_large_url(b):
    qset  = BusinessPhoto.objects.filter(business=b,is_default=True)
    if qset.count() < 1:
        return False
    ph = qset[0].image_large
    return ph.url



        
def add_photo_by_upload(img,b,user,default):
    bp = BusinessPhoto(user=user, business=b, image=img, title=b.name, caption=b.name,is_default=default)
    bp.save(True)
    return
    
def add_photo_by_url(phurl, b,user,default):
    outpath =settings.STATIC_ROOT+'img_dled.jpg'

    #print('retrieve'+str(urlparse.urlunparse(phurl)))
    urlretrieve(phurl, outpath)
    bp = BusinessPhoto(user=user, business=b, image=outpath, title=b.name, caption=b.name,is_default=default)
    try:
        bp.save(False)
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        logger.error("Unexpected error:" + str(sys.exc_info()[0]))
        pass
    return

def get_all_bus_photos(b):
    photos = BusinessPhoto.objects.filter(business=b)
    return photos

def bus_gallery(request,bus_id):
    print(bus_id)
    b = get_object_or_404(Business,pk=bus_id)
    print('bus gallery for ' + str(b.name))
    context = get_gallery_context(request.user)
    context.update({
        'business' : b,
        'photos' : get_all_bus_photos(b)
                    })
    template = 'photos/gallery.html'
    return render_to_response(template, RequestContext(request,context))

def full_gallery(request):
    print('full gallery')
    context = {}
    return redirect('ratings/', RequestContext(request,context))
    
    
