from BeautifulSoup import BeautifulStoneSoup
#from docserver.public_site.models import Document, DocumentLegislation
from django.core.management.base import NoArgsCommand
from django import db
from scrape_utils import *
import datetime
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        add_date=datetime.datetime.now()
        doc_type = "CRS"
        file_type = "pdf"
        
        for i in range(0,1):
            print "PAGE %s" % i
            url = "http://opencrs.com/recent/feed.xml?key=%s&page=%s" % (settings.OPEN_CRS_KEY, i)
            print url
            page = urllib2.urlopen(url)
            soup = BeautifulStoneSoup(page)
            for document in soup.documents.findAll('document'):
                db.reset_queries()
                order_code = document['order_code']
                release_date = document['release_date']
                gov_id = "CRS_%s_%s" % (order_code, release_date.replace('-', ''))
                title = document.title.contents[0]
                description = ' '
                doc = {'order_code':order_code, 'release_date':release_date, 'gov_id':gov_id, 'title':title, 'description':description}
                #incomplete
                #
                #
                #
                #