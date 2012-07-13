# Create your views here.
#for businesses


#gets thumb photo (small)
from comments.models import PhotoComment, Comment
from communities.models import Community
from communities.views import get_community
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.context import RequestContext
from photos.models import BusinessPhoto
from rateout import settings
from ratings.models import Business, CommentRating
from recommendation.normalization import getNumPosRatings, getNumNegRatings
from tags.models import Tag, HardTag
from tags.views import get_tags_user, get_top_tags, get_all_sorts
from urllib import urlretrieve
import json
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
    return bp
    
def add_photo_by_url(phurl, b,user,default):
    outpath =settings.STATIC_ROOT+str(b.id)+"_"+str(b.city)+"_"+str(b.state)
    #print('retrieve'+str(urlparse.urlunparse(phurl)))
    try:
        urlretrieve(phurl, outpath)
    except:
        return None
    bp = BusinessPhoto(user=user, business=b, image=outpath, title=b.name, caption=b.name,is_default=default)
    try:
        bp.save(False)
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        logger.error("Unexpected error:" + str(sys.exc_info()[0]))
        pass
    return bp




def add_photo_to_bus(request):
    print(request.POST)
    bid = request.POST['bid']
    try:
        b = Business.objects.get(id=bid)
    except:
        logger.error("error in getting business")
        
    bp = None
    if 'image' in request.FILES:
        img = request.FILES['image']
        bp = add_photo_by_upload(img,b,request.user,default=False)
    else:
        url = request.POST['url']
        if url != '':
            bp = add_photo_by_url(url, b, request.user, default=False)
    
    if bp:  
        context = {'p' :bp }
        return render_to_response('photos/photo.html',context)

    else:
        response_data= dict()
        response_data['empty'] = 'true'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    

def get_all_bus_photos(b):
    photos = BusinessPhoto.objects.filter(business=b)
    for p in photos:
        p.comment_list = get_top_photo_comments(p,5)
    
    return photos



#THIS IS A DUPLICATE
#XXX
def recurse_comments(comment,cur_list,even):
    cur_list.append(comment)
    replies = Comment.objects.filter(reply_to=comment).order_by('-date')
    for c in replies:
        if even:
            cur_list.append("open-even")
        else:
            cur_list.append("open-odd")
        recurse_comments(c,cur_list,not even)
        cur_list.append("close")

def get_top_photo_comments(photo,N):
    phcomments = PhotoComment.objects.filter(photo=photo)
    comment_list = []
    for pc in phcomments:
        if pc.thread.reply_to is None:
            c = pc.thread
            c.pos_ratings = getNumPosRatings(c)
            c.neg_ratings = getNumNegRatings(c)
            comment_list.append(c)
            

    sortedComments = sorted(comment_list, cmp = lambda l, r: cmp(l.pos_ratings, r.pos_ratings), reverse=True)
    return sortedComments[:N]

def get_photo_comments(photo,user=False):
    phcomments = PhotoComment.objects.filter(photo=photo).order_by('-date')

    comment_list = []
    for pc in phcomments:
        if pc.thread.reply_to is None: #root tag comment
            comment_list.append("open-even")
            recurse_comments(pc.thread,comment_list,False)
            comment_list.append("close")    
    results = []              
    for c in comment_list:
        if c != "open-even" and c != "open-odd" and c != "close":
            try:
                rat =  CommentRating.objects.get(comment=c)
                c.this_rat = rat.rating
                c.pos_ratings = getNumPosRatings(c)
                c.neg_ratings = getNumNegRatings(c)
            except:
                c.this_rat = 0
                c.pos_ratings = 0
                c.neg_ratings = 0
        results.append(c)
    return results


def  photo_detail(request,ph_id):
    photo = get_object_or_404(BusinessPhoto,pk=ph_id)
    print(photo)
    context = {
        'p' : photo,
        'comments': get_photo_comments(photo)
        }
    return render_to_response('photos/detail.html',RequestContext(request,context))
    




def bus_gallery(request,bus_id):
    b = get_object_or_404(Business,pk=bus_id)
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
    
    
