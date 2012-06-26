'''
Created on Jun 26, 2012

@author: zouf
'''

from django.forms.models import ModelForm
from tags.models import HardTag

class HardTagForm(ModelForm):
    class Meta:
        model = HardTag
        
