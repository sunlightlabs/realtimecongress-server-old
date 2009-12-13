from django.core.management.base import BaseCommand
from realtimecongress_server.congress.models import RollCall, Legislation, Legislator
from BeautifulSoup import BeautifulSoup
import urllib2

YEAR = 2009
INDEX_URL = "http://clerk.house.gov/evs/%s/index.asp"
INDEX_CHUNK_URL = "http://clerk.house.gov/evs/%s/ROLL_%s.asp"
ROLLCALL_URL = "http://clerk.house.gov/evs/%s/roll%s.xml"

FIELDS = ("number","date","issue","question","result","title")

def extract_text(node):
    s = node.contents[0].string
    if s is None:
        s = node.contents[0].contents[1].string
    return s
    
def rollcalls(year, chunk=None):
    if chunk:
        url = INDEX_CHUNK_URL % (year, chunk)
    else:
        url = INDEX_URL % year
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    for row in soup.find("table").findAll("tr"):
        if row.td:
            num = row.td.a.string
            try:
                RollCall.objects.get(number=num)
            except RollCall.DoesNotExist:
                yield int(num)

def parse_rollcall(year, number):
    print ROLLCALL_URL % (year, number)
                
class Command(BaseCommand):
    
    def handle(self, year, chunk=None, **options):
        for num in rollcalls(year, chunk):
            parse_rollcall(year, num)