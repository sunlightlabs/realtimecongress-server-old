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
        item_added = False; 
        
        def flush_cache():
            memc = memcache.Client(['127.0.0.1:11211'])
            memc.flush_all() #flush memcache

        def add_event(event):
            dupe = FloorEvent.objects.filter(date=event['event_time'], chamber=event['chamber'])
            if not dupe:
                event = FloorEvent(date=event['event_time'], description=event['description'], chamber=event['chamber'])
                event.save()
                item_added = True
        
        #handy string cleaning functions found at http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html
        def remove_extra_spaces(data):
            p = re.compile(r'\s+')
            return p.sub(' ', data)

        def remove_html_tags(data):
            p = re.compile(r'<.*?>')
            return p.sub('', data)
            
        chamber = "House"
        description = None
        event_time = None
  
        try:
            page = urllib2.urlopen("http://clerk.house.gov/floorsummary/floor.html")
        except:
            print "Error Loading Page %s" % sys.exc_info()[0]
        else:
            soup = BeautifulSoup(page)
            date_field = soup.findAll(text=re.compile('LEGISLATIVE DAY OF'))[0].strip()
            date_string = time.strftime("%m/%d/%Y", time.strptime(date_field.replace('LEGISLATIVE DAY OF ', ''), "%B %d, %Y"))
            
            rows = soup.findAll('dt')
            for row in rows:
                if row.b.contents:
                    time_string = row.b.contents[0]
                    t = re.compile("(\d+:\d{2}\s+(A|P)\.M\.)")
                    m = t.findall(time_string)
                    if m:
                        time_string = remove_extra_spaces(m[0][0].replace('.', ''))
                        time_string = "%s %s" % (date_string, time_string)
                        event_time = datetime.datetime(*time.strptime(time_string, "%m/%d/%Y %I:%M %p")[0:5])
                        description = remove_html_tags(remove_extra_spaces(str(row.findNextSibling()))).strip()
                        event = {'event_time':event_time, 'description':description, 'chamber':chamber}
                        print event
                        #add_event(event)
            #if item_added:
                #flush_cache()