from piston.handler import BaseHandler
from realtimecongress_server.congress.models import Legislator, Legislation, RollCall

class LegislatorHandler(BaseHandler):
    model = Legislator
    allowed_methods = ('GET',)

class LegislationHandler(BaseHandler):
    model = Legislation
    allowed_methods = ('GET',)