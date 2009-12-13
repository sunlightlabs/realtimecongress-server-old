from BeautifulSoup import BeautifulSoup, SoupStrainer
from congress_utils import extract_legislation, congress_from_year, clean_bill_num
#from rtc.mobile.models import FloorEvent
from django.core.management.base import NoArgsCommand
import datetime, time
import memcache
import re
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):

        chamber = "Senate"
        description = None
        event_time = None
        
        def flush_cache():
            memc = memcache.Client(['127.0.0.1:11211'])
            memc.flush_all() #flush memcache

        def add_event(event):
            dupe = FloorEvent.objects.filter(date=event['event_time'], chamber=event['chamber'])
            if not dupe:
                event = FloorEvent(date=event['event_time'], description=event['description'], chamber=event['chamber'], url=event['url'])
                event.save()
            else:
                print "dupe: %s" % event
  
        try:
            page = urllib2.urlopen("http://republican.senate.gov/public/index.cfm?FuseAction=FloorUpdates.Home")
        except:
            print "Error Loading Page %s" % sys.exc_info()[0]
        else:
            soup = BeautifulSoup(page)
            rows = soup.findAll('div', {'class':'EventCalendarEvent'})
            item_added = False
            for row in rows:
                time_str = row.strong.contents[0]
                date_str = row.a['href'].replace('index.cfm?FuseAction=FloorUpdates.Home&Date=', '').split('#')[0]
                datetime_str = "%s %s" % (date_str, time_str)
                event_time = datetime.datetime(*time.strptime(datetime_str, "%d-%b-%y %I:%M %p")[0:6])
                description = row.a.contents[0].replace('Floor -- ', '')
                url = "http://republican.senate.gov/%s" % row.a['href']
                event = {'event_time':event_time, 'description':description, 'chamber':chamber, 'url':url}
                print event
                #add_event(event)
        #if item_added:
            #flush_cache()