from django.core.management.base import NoArgsCommand
#from rtc.mobile.models import WhipNotice
import datetime, time
import feedparser
#import memcache
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        item_added = False

        def flush_cache():
            memc = memcache.Client(['127.0.0.1:11211'])
            memc.flush_all() #flush memcache
        
        def update_docs(source):
            d = feedparser.parse(FEED_URL[source])
            items = d['items']
            for item in items:
                url = item.link.replace('&amp;', '&');
                if not hasattr(item, 'updated_parsed'):
                    pubdate = None
                else:
                    pubdate = datetime.datetime(*item.updated_parsed[:6])
            
                if not hasattr(item, 'id'):
                    item.id = url
                
                doc = {'id':item.id, 'pubdate':pubdate, 'url':url, 'doc_type':source}
                print doc
             
                #dupe = WhipNotice.objects.filter(url=url)
                #dupes = WhipNotice.objects.filter(date=pubdate, doc_type=source)
                #if len(dupes) == 0:
                #    notice = WhipNotice(date=pubdate, url=url, doc_type=source)
                #    notice.save()
                #    item_added = True
                
        prefix = 'http://majoritywhip.house.gov/'
        FEED_URL = {'dwd':"%s?a=RSS.Feed&Type=TheDailyWhipline" % prefix,
            'dww':"%s?a=RSS.Feed&Type=TheDailyWhipPack" % prefix}
                    
        for k,v in FEED_URL.items():
            update_docs(k)
        
        #if item_added:
        #    flush_cache()