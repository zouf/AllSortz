'''
Created on Jun 12, 2012

@author: zouf
'''
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet
from ratings.models import Tag
import sys



def search_site(term):
    search_results = (SearchQuerySet().filter(content=term))
    businesses = []
    for sr in search_results:
        print(sr.model_name)
        if sr.model_name == "business":
            businesses.append(sr.object)
        elif sr.model_name == "tag":
            businesses.append(sr.object.business)
        else:
            print('error')
    return businesses   


def N_recent_results(term,N):
    recent_results = SearchQuerySet().filter(content=term).order_by('-pub_date')[:N]
    results = []
    for sr in recent_results:
        
        t = Tag.objects.get(pk=sr.pk)
        results.append(t.business)
    return results   