'''
Created on Jun 12, 2012

@author: zouf
'''
from communities.models import BusinessMembership
from ratings.models import Business
from tags.models import Tag, BusinessTag
import logging
#from haystack.query import SearchQuerySet

logger = logging.getLogger(__name__)

def search_site(searchTerm, locationTerm):
    
    logger.debug("Searching for "+str(searchTerm) + " near " + str(locationTerm))
    print("Searching for "+str(searchTerm) + " near " + str(locationTerm))
#    search_results = (SearchQuerySet().filter(content=searchTerm))
    
    q = searchTerm
    
    
    businesses = []
    
    
    queryset = Business.objects.extra(where=['name @@ plainto_tsquery(%s)'], params=[q])
    for entry in queryset:
        businesses.append(entry)
        
    tagset = Tag.objects.extra(where=['descr @@ plainto_tsquery(%s)'], params=[q])
    for entry in tagset:
        bt = BusinessTag.objects.filter(tag=entry)
        for b in bt:
            businesses.append(b.business)
            
    return businesses

    
    
    
    
        
        
        


def get_all_nearby(mylat,mylng,distance=1):

    current_pg_point = "point '({:.5f}, {:.5f})'".format(mylng, mylat)
    buses_query = " ".join(["SELECT *",
                                    "FROM (SELECT id, (point(lon, lat) <@> {}) AS dist FROM ratings_business) AS dists",
                                    "WHERE dist <= {:4f} ORDER BY dist ASC;"]).format(current_pg_point, distance)
    buses = Business.objects.raw(buses_query)
    return buses

  

def in_location(bus, locations):
    for l in locations:
        res = BusinessMembership.objects.filter(community = l, business = bus)
        if res.count() > 0:
            return True
    return False

#def N_recent_results(term,N):
#    recent_results = SearchQuerySet().filter(content=term).order_by('-pub_date')[:N]
#    results = []
#    for sr in recent_results:
#        
#        t = Tag.objects.get(pk=sr.pk)
#        results.append(t.business)
#    return results   

