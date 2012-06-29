'''
Created on Jun 4, 2012

@author: zouf
'''
from haystack import indexes
from ratings.models import Business, Comment

    
class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Business

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    


    
class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Comment

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    


