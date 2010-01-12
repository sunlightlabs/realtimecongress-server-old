from BeautifulSoup import BeautifulSoup, SoupStrainer
from congress_utils import extract_legislation, congress_from_year, clean_bill_num
from django.core.management.base import NoArgsCommand
from scrape_utils import *
import datetime, time
import re
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        url = 'http://thomas.loc.gov/help/terms-subjects.html'
        page = urllib2.urlopen(url)
        timestamp = datetime.datetime.now()
        
        soup = BeautifulSoup(page)
        rows = soup.findAll('p').find('strong')
        print rows
        
