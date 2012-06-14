'''
Created on Jun 4, 2012

@author: zouf
'''
from comments.models import Comment
from haystack import indexes

    
class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Comment

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
