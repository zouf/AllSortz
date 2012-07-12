'''
Created on Jun 12, 2012

@author: zouf
'''
from communities.models import BusinessMembership, Community
from geopy import geocoders
from haystack.query import SearchQuerySet
from ratings.models import Business
from tags.models import Tag, BusinessTag
import logging

logger = logging.getLogger(__name__)

def search_site(searchTerm, locationTerm):
    
    logger.debug("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    print("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    search_results = (SearchQuerySet().filter(content=searchTerm))
    
    try:
        c=Community.objects.get(name=locationTerm)
    except:
        logger.error('community object not found!')
    
    g = geocoders.Google()  
    res = g.geocode(str(c.city) +', '+str(c.state),exactly_one=False)
    place, (base_lat,base_lng) = res[0]
    #print "%s: %.5f, %.5f" % (place, base_lat, base_lng)  
    
    businesses = []
    for sr in search_results:
        bus = None            
        if sr.model_name == "business":            
            bus = sr.object
            distance = 3
            current_pg_point = "point '({:.5f}, {:.5f})'".format(base_lng, base_lat)
            
            buses_query = " ".join(["SELECT *",
                                    "FROM (SELECT id, (coordinates <@> {}) AS dist FROM ratings_business) AS dists",
                                    "WHERE dist <= {:4f} ORDER BY dist ASC;"]).format(current_pg_point, distance)
            buses = Business.objects.raw(buses_query)
            for bresult in buses:
                if bresult.id == bus.id:
                    businesses.append(bus)
        elif sr.model_name == "tag":
            bustags = BusinessTag.objects.filter(tag=sr.object)
            for bt in bustags:
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

