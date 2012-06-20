
from django.forms import ModelForm
from ratings.models import Business, Comment


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        
