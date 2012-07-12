'''
Created on Jun 4, 2012

@author: zouf
'''
from haystack import indexes
from ratings.models import Business

    
class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Business

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    


