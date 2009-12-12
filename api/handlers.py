from piston.handler import BaseHandler
from realtimecongress_server.congress.models import Legislator, Legislation, RollCall

class LegislatorHandler(BaseHandler):
    model = Legislator
    fields = ('title','first_name','last_name','suffix','nickname',
              'district','state','party','gender','currently_serving',
              'govtrack_id','bioguide_id','display_name')
    allowed_methods = ('GET',)
    
    def read(self, request):
        qs = Legislator.objects.all()
        if 'state' in request.GET:
            qs = qs.filter(state=request.GET['state'].upper())
        if 'party' in request.GET:
            qs = qs.filter(party=request.GET['party'].upper())
        if 'currently_serving' in request.GET:
            qs = qs.filter(currently_serving=request.GET['currently_serving'] != '0')
        return qs

class LegislationHandler(BaseHandler):
    model = Legislation
    fields = ('code','congress','title','summary','chamber','introduced',
              ('sponsor', ('display_name','govtrack_id')),
              ('co_sponsors', ('display_name','govtrack_id')),
              'actions')
    allowed_methods = ('GET',)

class RollCallHandler(BaseHandler):
    model = RollCall
    fields = ('legislation','datestamp',
              ('votes', ('vote', ('legislator', ('display_name','govtrack_id')),)))
    allowed_methods = ('GET',)