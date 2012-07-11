'''
Created on Jun 12, 2012

@author: zouf
'''
from communities.models import BusinessMembership, Community
from haystack.query import SearchQuerySet
from ratings.models import Business
from tags.models import Tag, BusinessTag
import logging

logger = logging.getLogger(__name__)

def search_site(searchTerm, locationTerm):
    
    logger.debug("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    print("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    search_results = (SearchQuerySet().filter(content=searchTerm))
    
    print(search_results)
    #location_results = (SearchQuerySet().filter(content=locationTerm))
    #locations = []
    #for l in location_results:
    #    if l.model_name == "community":
    #        locations.append(l.object)
    
    try:
        c=Community.objects.get(name=locationTerm)
    except:
        logger.error('community object not found!')
        
    
    print('community')
    print(c)
    businesses = []
    for sr in search_results:
        bus = None
        if sr.model_name == "business":
            bus = sr.object
            lon = -74.699607
            lat = 40.32551
            distance = 3
            current_pg_point = "point '({:.5f}, {:.5f})'".format(lon, lat)
            buses_query = " ".join(["SELECT *",
                                    "FROM (SELECT id, (coordinates <@> {}) AS dist FROM ratings_business) AS dists",
                                    "WHERE dist <= {:4f} ORDER BY dist ASC;"]).format(current_pg_point, distance)
            buses = Business.objects.raw(buses_query)

            buses = Business.objects.raw(buses_query)
            i=0
            for bb in buses:
                i+=1
                print('\nbus: ')
                print(bb)
            print(str(i) + " results")
            businesses.append(bus)
            print('done here')
        elif sr.model_name == "tag":
            bustags = BusinessTag.objects.filter(tag=sr.object)
            for bt in bustags:
                print(bt)
                businesses.append(bt.business)
        elif sr.model_name == "comment":
            bus = sr.object.business
            businesses.append(bus)
        else:
            print('error')
            logger.error('error in search_site')
        
        #if in_location(bus,locations):
        
    
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

