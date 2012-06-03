
from django.forms import ModelForm
from ratings.models import Business


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        
