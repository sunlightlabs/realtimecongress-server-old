from BeautifulSoup import BeautifulSoup
from django.core.management.base import NoArgsCommand
#from rtc.mobile.models import CommitteeMeeting
import datetime, time
import feedparser
import memcache
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):

        def flush_cache():
            memc = memcache.Client(['127.0.0.1:11211'])
            memc.flush_all() #flush memcache
            
        d = feedparser.parse("http://www.govtrack.us/users/events-rss2.xpd?monitors=misc:allcommittee")
        item_added = False
        items = d['items']
        for item in items:
            url = item.link.replace('&amp;', '&');
            title_str = item.title.replace('Committee Hearing: ', '')
            description = item.description
            chamber = title_str.partition(' ')[0]
            committee = title_str.partition(' ')[2]
            if chamber == "House":
                room = None
                cmte_code = None
                title_str = title_str.partition(' ')[2]
                soup = BeautifulSoup(description)
                p = soup.findAll('p')[0].contents[0]
                title = p.split(' -- ')[0].strip()
                date_str = p.split(' -- ')[1].replace(' at ', ' ').replace('a.m', 'AM').replace('p.m.', 'PM').replace('.', '').strip()
                try:
                    meeting_date = datetime.datetime(*time.strptime(date_str, "%b %d, %Y %I:%M %p")[0:6])
                except:
                    meeting_date = datetime.datetime(*time.strptime(date_str, "%b %d, %Y %I %p")[0:5])
                
                event = {'chamber':chamber, 'url':url, 'description':description, 'room':room, 'committee':committee, 
                    'cmte_code':cmte_code, 'title':title, 'meeting_date':meeting_date}
                print event
                #dupes = CommitteeMeeting.objects.filter(committee=committee).filter(date=meeting_date)
                #if dupes:
                #    dupe = dupes[0]
                #    dupe.matter = title
                #    dupe.save()
                #else:
                #    meeting = CommitteeMeeting(chamber=chamber, committee=committee,
                #        date=meeting_date, room=room, matter=title)
                #    meeting.save()
                #    item_added = True
            
            #if item_added:
                #flush_cache()