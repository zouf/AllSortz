from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USStateField
from ratings.models import Keyword
from ratings.models import Business

RATING_CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
)

class RatingForm(forms.Form):
	rating = forms.ChoiceField(choices=RATING_CHOICES)


class BusinessForm(ModelForm):
	class Meta:
	        model = Business
	        #exclude = ('keywords',)
	



class KeywordForm(ModelForm):
	class Meta:
	        model = Keyword