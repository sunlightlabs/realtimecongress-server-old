from django.core.management.base import NoArgsCommand
from realtimecongress_server.congress.models import Legislator
import csv
import datetime
import urllib2

DATA_URL = "http://github.com/sunlightlabs/apidata/raw/master/legislators/legislators.csv"

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        res = urllib2.urlopen(DATA_URL)
        reader = csv.DictReader(res)
        
        for record in reader:
            
            bioguide_id = record['bioguide_id'] or None
            
            if bioguide_id is not None:
                
                try:
                    l = Legislator.objects.get(bioguide_id=bioguide_id)
                except Legislator.DoesNotExist:
                    l = Legislator(bioguide_id=bioguide_id)
            
                l.title = record['title']
                l.first_name = record['firstname']
                l.last_name = record['lastname']
                l.suffix = record['name_suffix']
                l.nickname = record['nickname']
                l.district = record['district']
                l.state = record['state']
                l.party = record['party']
                l.gender = record['gender']
                l.currently_serving = record['in_office'] == '1'
                l.govtrack_id = record['govtrack_id']
                
                l.save()
            
            else:
                
                print "no govtrack_id for %s %s (%s)" % (record['firstname'], record['lastname'], record['state'])
    
        res.close()