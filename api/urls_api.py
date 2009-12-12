from django.conf.urls.defaults import *
from piston.emitters import Emitter
from piston.resource import Resource
from realtimecongress_server.handlers import *

# congress endpoints
urlpatterns = patterns('',
    url(r'^legislators.(?P<emitter_format>.+)$', Resource(LegislatorHandler)),
    url(r'^legislation.(?P<emitter_format>.+)$', Resource(LegislationHandler)),
)
