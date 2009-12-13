from BeautifulSoup import BeautifulSoup, SoupStrainer
from congress_utils import extract_legislation, congress_from_year, clean_bill_num
#from rtc.mobile.models import WhipNotice
from django.core.management.base import NoArgsCommand
import datetime, time
import memcache
import re
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        daily_title = 'The Whipping Post - '
        weekly_title = 'The Whip Notice - Week of '
        
        def single_digify(date_str):
            m_str = date_str.split('-')[0]
            d_str = date_str.split('-')[1].lstrip('0')
            y_str = date_str.split('-')[2]
            return "%s-%s-%s" % (m_str, d_str, y_str)

        def flush_cache():
            memc = memcache.Client(['127.0.0.1:11211'])
            memc.flush_all() #flush memcache        
        
        #handy string cleaning functions found at http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html
        def remove_extra_spaces(data):
            p = re.compile(r'\s+')
            return p.sub(' ', data)

        def remove_html_tags(data):
            p = re.compile(r'<.*?>')
            return p.sub('', data)
  
        try:
            page = urllib2.urlopen("http://republicanwhip.house.gov/floor/")
        except:
            print "Error Loading Page %s" % sys.exc_info()[0]
        else:
            soup = BeautifulSoup(page)
            titles = soup.findAll('span', {'class':'WHIP_FONT_2'})
            
            item_added = False
            for title in titles:
                daily_re = re.compile(daily_title)
                weekly_re = re.compile(weekly_title)
                title_str = title.contents[0].strip()
                if weekly_re.match(title_str):
                    weekly_date_str = title_str.replace(weekly_title, '').strip()
                    weekly_date = meeting_date = datetime.datetime(*time.strptime(weekly_date_str, "%m/%d/%y")[0:6])
                    weekly_url = "http://republicanwhip.house.gov/floor/%s.pdf" % single_digify(weekly_date.strftime("%m-%d-%y"))
                    doc = {'date':weekly_date, 'url':weekly_url, 'doc_type':'rww'}
                    
                    #dupes = WhipNotice.objects.filter(date=weekly_date, doc_type="rww")
                    #if len(dupes) == 0:
                    #    notice = WhipNotice(date=weekly_date, url=weekly_url, doc_type="rww")
                    #    notice.save()
                    
                elif daily_re.match(title_str):
                    daily_date_str = title_str.replace(daily_title, '').strip()
                    daily_date = meeting_date = datetime.datetime(*time.strptime(daily_date_str, "%m/%d/%y")[0:6])
                    daily_url = "http://republicanwhip.house.gov/floor/%s.pdf" % single_digify(daily_date.strftime("%m-%d-%y"))
                    doc = {'date':daily_date, 'url':daily_url, 'doc_type':'rwd'}
                    #dupes = WhipNotice.objects.filter(date=daily_date, doc_type="rwd")
                    #if len(dupes) == 0:
                    #    notice = WhipNotice(date=daily_date, url=daily_url, doc_type="rwd")
                    #    notice.save()
                    #    item_added = True
                print doc
            #if item_added:
                #flush_cache()