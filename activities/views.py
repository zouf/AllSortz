# Create your views here.
from activities.forms import ActivityForm, ActivityWaypointForm
from activities.models import Activity, ActivityWaypoint
from communities.models import BusinessMembership, Community
from communities.views import get_community
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from photos.models import BusinessPhoto
from ratings.forms import BusinessForm
from ratings.models import Business
from ratings.populate import create_business
from ratings.utility import get_bus_data, get_avg_latlng
from ratings.views import detail_keywords, paginate_businesses
import activities
import logging


logger = logging.getLogger(__name__)


def get_activites(community):
    if community is not None:
        return Activity.objects.filter(community=community)
    return Activity.objects.all()

def create_activity(name,creator,descr,start,end,community):
    act = Activity(name=name,creator=creator,descr=descr,start=start,end=end,community=community, number_of_items=0)
    return act

def add_to_activity(activity, business):
    pos = activity.number_of_items
    aw = ActivityWaypoint(business=business,activity=activity,position=pos)
    activity.number_of_items +=1
    activity.save()
    return aw


def add_activity(request):
 
    if request.method == 'POST':  # add a business
        form = ActivityForm(request.POST, request.FILES)
        name = form.data['name']
        logger.debug("Creation of business %s by  %s", name,request.user.username)
        descr = form.data['descr']
        start = form.data['start']
        end = form.data['end']
        cid = form.data['community']
        community = Community.objects.get(id=cid)
        
        act = create_activity(name=name,creator=request.user, descr=descr,community = community, start=start,end=end)
        act.save()
    
        community = get_community(request.user)

        return activities(request)
    else:  # Print a boring business form
        f = ActivityForm()
        return render_to_response('activities/add_activity.html', {'form': f}, context_instance=RequestContext(request))



def detail_activity(request, act_id):
    activity = get_object_or_404(Activity, pk=act_id)
    
    if request.method == 'POST':  # add a business
        form = ActivityWaypointForm(request.POST, request.FILES)
        business = Business.objects.get(id=form.data['business'])
        aw = add_to_activity(activity,business)
        aw.save()
    waypoints = ActivityWaypoint.objects.filter(activity=activity)
    business_list = get_bus_data(Business.objects.all(),request.user)
    business_list = paginate_businesses(business_list,request.GET.get('page'),5)
    waypoint_form = ActivityWaypointForm()
    latlng = get_avg_latlng(business_list)   
    
    return render_to_response('activities/detail.html', {'businesses':Business.objects.all(), 'waypoint_form': waypoint_form, 'waypoints':waypoints, 'activity': activity,'business_list':business_list, 'baselat':latlng[0], 'baselng':latlng[1]}, context_instance=RequestContext(request))



def activities(request):
    
    community = get_community(request.user)
    businesses = []
    try:
        busMembership = BusinessMembership.objects.filter(community = community)
        for b in busMembership:
            businesses.append(b.business)
    except:
        logger.debug("error in getting businesses community, maybe businesses wasnt put in community?")
        businesses = Business.objects.all()
    
    activities = get_activites(community)
    paginator = Paginator(activities, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        activities = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)
    return render_to_response('activities/activities.html', {'activities': activities, 'community':community}, context_instance=RequestContext(request))