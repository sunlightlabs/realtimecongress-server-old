from BeautifulSoup import BeautifulStoneSoup
from django.core.management.base import NoArgsCommand
#from rtc.mobile.models import CommitteeMeeting
import datetime, time
import memcache
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        def flush_cache():
            memc = memcache.Client(['127.0.0.1:11211'])
            memc.flush_all() #flush memcache
            
        chamber = "Senate"
        page = urllib2.urlopen("http://www.senate.gov/general/committee_schedules/hearings.xml")
        soup = BeautifulStoneSoup(page)
        meetings = soup.findAll('meeting')
        item_added = False
        event_type = 'hearing'
        
        for meeting in meetings:
            cmte_code = meeting.cmte_code.contents[0].strip()
            committee = meeting.committee.contents[0].strip()
            date_string = meeting.date.contents[0].strip()
            meeting_date = datetime.datetime(*time.strptime(date_string, "%d-%b-%Y %H:%M %p")[0:6])
            if meeting_date.hour < 6:
               d = datetime.timedelta(hours=12)
               meeting_date = meeting_date + d
            room = meeting.room.contents[0].strip()
            matter = meeting.matter.contents[0].strip().replace('\n', '')
            event = {'event_type':event_type, 'cmte_code':cmte_code, 'committee':committee, 'meeting_date':meeting_date,
                        'room':room, 'matter':matter}
            print event
            
            #dupes = CommitteeMeeting.objects.filter(committee_code=cmte_code).filter(date=meeting_date)
            #if dupes:
            #    dupe = dupes[0]
            #    dupe.room = room
            #    dupe.matter = matter
            #    dupe.save()
            #else:
            #    if cmte_code.strip() != "":
            #        meeting = CommitteeMeeting(chamber=chamber, committee_code=cmte_code, committee=committee,
            #            date=meeting_date, room=room, matter=matter)
            #        meeting.save()
            #        item_added = True
                    
        #if item_added:
            #flush_cache()