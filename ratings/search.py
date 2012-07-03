'''
Created on Jun 12, 2012

@author: zouf
'''
from haystack.query import SearchQuerySet
from tags.models import Tag
import logging
from communities.models import BusinessMembership

logger = logging.getLogger(__name__)

def search_site(searchTerm, locationTerm):
    
    logger.debug("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    print("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    search_results = (SearchQuerySet().filter(content=searchTerm))
    
    print(search_results)
    location_results = (SearchQuerySet().filter(content=locationTerm))
    locations = []
    for l in location_results:
        if l.model_name == "community":
            locations.append(l.object)
    
    businesses = []
    for sr in search_results:
        bus = None
        print(sr)
        if sr.model_name == "business":
            bus = sr.object
        elif sr.model_name == "tag":
            bus = sr.object.business
        elif sr.model_name == "comment":
            bus = sr.object.business
        else:
            logger.error('error in search_site')
        
        #if in_location(bus,locations):
        businesses.append(bus)
    
    return businesses   


def in_location(bus, locations):
    for l in locations:
        res = BusinessMembership.objects.filter(community = l, business = bus)
        if res.count() > 0:
            return True
    return False

def N_recent_results(term,N):
    recent_results = SearchQuerySet().filter(content=term).order_by('-pub_date')[:N]
    results = []
    for sr in recent_results:
        
        t = Tag.objects.get(pk=sr.pk)
        results.append(t.business)
    return results   

