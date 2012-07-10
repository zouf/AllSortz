from django.contrib import admin
from ratings.models import Business, Rating


#class GroupingInline(admin.TabularInline):
#    model = Grouping
#    extra = 1
#
#
#class KeywordAdmin(admin.ModelAdmin):
#    inlines = (GroupingInline,)
#
#
#class BusinessAdmin(admin.ModelAdmin):
#    inlines = (GroupingInline,)
#
#admin.site.register(Keyword, KeywordAdmin)
#admin.site.register(Rating)
#admin.site.register(Business, BusinessAdmin)
#admin.site.register(Grouping)


class BusinessAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'date',)
    list_filter = ('name', 'date',)

admin.site.register(Business, BusinessAdmin)
