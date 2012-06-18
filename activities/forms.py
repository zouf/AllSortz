'''
Created on Jun 18, 2012

@author: zouf
'''
from activities.models import Activity, ActivityWaypoint
from django.contrib.localflavor.generic.forms import DateTimeField
from django.forms.models import ModelForm
from django.forms.widgets import SplitDateTimeWidget


class ActivityForm(ModelForm):
    class Meta:
        model = Activity

class ActivityWaypointForm(ModelForm):
    class Meta:
        model = ActivityWaypoint