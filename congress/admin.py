from django.contrib import admin
from realtimecongress_server.congress.models import *

# legislator

class LegislatorAdmin(admin.ModelAdmin):
    list_display = ('display_name','nickname','party','state','district','currently_serving','govtrack_id')
    list_filter = ('party','currently_serving','title','state')
    search_fields = ('first_name','last_name','nickname','govtrack_id')
admin.site.register(Legislator, LegislatorAdmin)

# legislation

class ActionInline(admin.TabularInline):
    model = Action

class LegislationAdmin(admin.ModelAdmin):
    inlines = (ActionInline,)
    list_display = ('code','title','congress','introduced')
    list_filter = ('chamber','congress')
    list_search = ('code','title')
admin.site.register(Legislation, LegislationAdmin)

# roll call

class VoteInline(admin.TabularInline):
    model = Vote

class RollCallAdmin(admin.ModelAdmin):
    inlines = (VoteInline,)
    #list_display = ('legislation__title','datestamp')
admin.site.register(RollCall, RollCallAdmin)