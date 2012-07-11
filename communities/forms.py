'''
Created on Jun 27, 2012

@author: zouf
'''
from communities.models import Community
from django.forms.models import ModelForm

class CommunityForm(ModelForm):
    class Meta:
        model = Community
        
