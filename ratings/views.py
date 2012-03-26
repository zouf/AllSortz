from ratings.models import Business
from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.views.generic import DetailView, ListView
from django.shortcuts import render_to_response, get_object_or_404

def detail(request, bus_id):
    p = get_object_or_404(Business, pk=bus_id)
    return render_to_response('ratings/detail.html', {'business': p},
                               context_instance=RequestContext(request))

def rate(request, bus_id):
    return HttpResponse("You're rating for business %s." % bus_id)

def index(request):
    business_list = Business.objects.all()
    t = loader.get_template('ratings/index.html')
    c = Context({
        'business_list': business_list,
    })
    return HttpResponse(t.render(c))