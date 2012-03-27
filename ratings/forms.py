from django import forms


RATING_CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
)

class RatingForm(forms.Form):
	rating = forms.ChoiceField(choices=RATING_CHOICES)
#	rating = forms.DecimalField()