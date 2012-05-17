from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USStateField
from ratings.models import Keyword
from ratings.models import Business

RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
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