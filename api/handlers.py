from piston.handler import BaseHandler
from realtimecongress_server.congress.models import Legislator, Legislation, RollCall

class LegislatorHandler(BaseHandler):
    model = Legislator
    fields = ('title','first_name','last_name','suffix','nickname',
              'district','state','','','','',
        ('sponsor', ('display_name','govtrack_id')),
        ('co_sponsors', ('display_name','govtrack_id')),
        'actions')
    allowed_methods = ('GET',)

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
        ('votes', ('vote', ('legislator', ('display_name','govtrack_id')),))
        )
    allowed_methods = ('GET',)