from ratings.models import Business
from ratings.models import Rating
from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.views.generic import DetailView, ListView
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from ratings.forms import RatingForm
from django.db.models import F




def detail(request, bus_id):

	if request.user.is_authenticated():
		b = get_object_or_404(Business, pk=bus_id)
		r = Rating.objects.get(username=request.user, business=bus_id)
		if request.method == 'POST':  #display rating if it exists
			form = RatingForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				new_rating = cd['rating']
				r.rating  = new_rating
				r.save() 
		f2 = RatingForm();
		
		return render_to_response('ratings/detail.html', {'business': b,'rating': r, 'form' : f2}, context_instance=RequestContext(request))    
	else:
		p = get_object_or_404(Business, pk=bus_id)
		return render_to_response('ratings/detail.html', {'business': p}, context_instance=RequestContext(request))
		
		
		

def rate(request, bus_id):
    return HttpResponse("You're rating for business %s." % bus_id)

def index(request):
	if request.user.is_authenticated():
		business_list = Business.objects.all()
		t = loader.get_template('index.html')
		c = Context({
		  'business_list': business_list,
		})
		return HttpResponse(t.render(c))
	else:
		return HttpResponse("log in dawg");
   




def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def portal_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    return render_to_response('/index.html')