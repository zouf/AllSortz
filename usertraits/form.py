'''
Created on Jun 28, 2012

@author: zouf
'''
from django.forms.models import ModelForm
from usertraits.models import Trait

class TraitForm(ModelForm):
    class Meta:
        model = Trait
        
