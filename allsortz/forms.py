from comments.models import Comment
from django.forms import ModelForm
from ratings.models import Business


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        
