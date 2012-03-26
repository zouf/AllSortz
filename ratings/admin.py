from ratings.models import Business
from ratings.models import Rating
from ratings.models import Grouping
from ratings.models import Keyword
from django.contrib import admin

class GroupingInline(admin.TabularInline):
    model = Grouping
    extra = 1

class KeywordAdmin(admin.ModelAdmin):
    inlines = (GroupingInline,)

class BusinessAdmin(admin.ModelAdmin):
    inlines = (GroupingInline,)

admin.site.register(Keyword,KeywordAdmin)
admin.site.register(Rating)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Grouping)
