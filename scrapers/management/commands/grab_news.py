from django.core.management.base import NoArgsCommand
#from rtc.mobile.models import NewsItem
import datetime, time
import feedparser
import memcache
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):

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
             
                news = {'id':item.id, 'date':pubdate, 'url':url, 'source':source, 'title':item.title}
                print news
                #newsitem = NewsItem(id=item.id, date=pubdate, url=url, source=source, title=item.title)
                #newsitem.save()
                #flush_cache()
                    
        for k,v in FEED_URL.items():
            update_docs(k)
        
FEED_URL = {'thehill':'http://thehill.com/homenews/senate?format=feed&amp;type=rss',
    'hotline':'http://hotlineoncall.nationaljournal.com/rss.xml',
    'nyt':'http://topics.nytimes.com/top/reference/timestopics/organizations/c/congress/index.html?rss=1',
    'thenote':'http://feeds.feedburner.com/ABCNews_TheNote?format=xml',
    'opencongress':'http://feeds.feedburner.com/OpenCongressCongressGossipBlog',
    'thepage':'http://feeds.feedburner.com/time/thepage?format=xml',
    'politico':'http://www.politico.com/rss/congress.xml',
    'rollcall':'http://www.rollcall.com/news/breakingnews.xml',
    'washpost':'http://feeds.voices.washingtonpost.com/wp/capitol-briefing/index',
}