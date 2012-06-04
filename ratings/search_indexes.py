'''
Created on Jun 4, 2012

@author: zouf
'''

from haystack import indexes
from ratings.models import Tag


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)


    def get_model(self):
        return Tag
#
#    def index_queryset(self):
#        """Used when the entire index for model is updated."""
#        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())