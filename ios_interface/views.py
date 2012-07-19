# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from httplib import HTTPResponse
from ratings.models import Business
import json

def get_businesses(request):
    data = serializers.serialize("xml", Business.objects.all())
    #response_data['businesses'] = json.dump(businesses)
    return HttpResponse(json.dumps(data), mimetype="application/json")
