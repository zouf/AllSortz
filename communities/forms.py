'''
Created on Jun 27, 2012

@author: zouf
'''
from django.forms.models import ModelForm
from ratings.models import Community

class CommunityForm(ModelForm):
    class Meta:
        model = Community
        
