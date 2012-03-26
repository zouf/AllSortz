from django.template import Context, loader
from ratings.models import Business
from django.http import HttpResponse


def detail(request, bus_id):
    return HttpResponse("You're looking at business %s." % bus_id)


def rate(request, bus_id):
    return HttpResponse("You're rating for business %s." % bus_id)

def index(request):
    business_list = Business.objects.all()
    t = loader.get_template('ratings/index.html')
    c = Context({
        'business_list': business_list,
    })
    return HttpResponse(t.render(c))