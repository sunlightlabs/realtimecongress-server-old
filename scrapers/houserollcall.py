import urlparse
import urllib2
import BeautifulSoup
import datetime
import sys
import re

HOUSE_ROLL_CALL_BASE = 'http://clerk.house.gov/evs/'
HOUSE_ROLL_CALL_START = 'index.asp'
DEBUG = True
RESULT_CODES = [u'Passed', u'Failed', u'Agreed']
RESULT_CODE_MAP = [u'P', u'F', u'A']
RESULT_PASSED = RESULT_CODES.index(u'Passed')
RESULT_FAILED = RESULT_CODES.index(u'Failed')
RESULT_AGREED = RESULT_CODES.index(u'Agreed')
YEAR_RE = re.compile(r'\(([12][0-9]{3})\)')

class Scraper(object):
    def __init__(self, debug=DEBUG):
        self.__debug__ = debug
        self.debug('Initializing House of Reps roll call scraper...')

    def debug(self, message):
        if self.__debug__:
            sys.stderr.write(message)
            sys.stderr.write('\n')

    def get_rolls(self, base_dict={}, url_tail=HOUSE_ROLL_CALL_START):
        # Compose URL to grab
        url = urlparse.urljoin(HOUSE_ROLL_CALL_BASE, 
                               str(datetime.date.today().year)+'/')
        url = urlparse.urljoin(url, url_tail)
        self.debug('Accessing %s' % url)
        response_obj = urllib2.urlopen(url)
        self.debug('Result: %d' % response_obj.code)
        house_data = response_obj.read()
        self.debug('%d bytes returned' % len(house_data))
        soup = BeautifulSoup.BeautifulSoup(house_data)
        # The year for the dates is in the heading in parentheses
        year = int(YEAR_RE.search(soup.find(name='h2').prettify()).group(1))
        table_node = soup.find(name='table')
        table_rows = table_node.findAll(name='tr')
        # toss the first row -- nothing but headers, but validate to make sure
        # the format hasn't changed
        table_headers = table_rows[0]
        table_headers = map(lambda font_node: font_node.contents[0],
                            table_headers.findAll(name='font'))
        assert table_headers == [u'Roll',
                                 u'Date',
                                 u'Issue',
                                 u'Question',
                                 u'Result',
                                 u'Title/Description']
        self.debug('Headers are as expected.')
        to_return = base_dict
        for row in table_rows[1:]:
            row_dict = {}
            # elements are as above in the tuple
            td_nodes = row.findAll(name='td')
            # first is the link to the roll call and the roll call ID
            row_dict['link'] = td_nodes[0].find(name='a')['href']
            row_dict['id'] = int(td_nodes[0].find(name='a').contents[0])
            self.debug('Processing roll call #%d' % row_dict['id'])
            # second is date -- process to datetime.date
            date_string = td_nodes[1].find(name='font').contents[0]
            # append the known year
            date_string += '-%d' % year
            date_obj = datetime.datetime.strptime(date_string,
                                                  '%d-%b-%Y')
            row_dict['date'] = date_obj.date()
            # third is issue
            # Not all issues have a link, and some don't even have an issue
            try:
                row_dict['issue_link'] = td_nodes[2].find(name='a')['href']
                row_dict['issue'] = td_nodes[2].find(name='a').contents[0]
            except TypeError:
                row_dict['issue_link'] = None
                try:
                    row_dict['issue'] = td_nodes[2].find(name='font').contents[0]
                except IndexError:
                    row_dict['issue'] = None
            # fourth is question
            row_dict['question'] = td_nodes[3].find(name='font').contents[0]
            # fifth is result -- use an integer index in RESULT_CODES
            row_dict['result'] = RESULT_CODE_MAP.index(
                td_nodes[4].find(name='font').contents[0])
            # last is title/description
            row_dict['title'] = td_nodes[5].find(name='font').contents[0]
            # add to to_return dictionary
            to_return[row_dict['id']] = row_dict
            self.debug('Success.')
        self.debug('Looking for links to other roll call lists...')
        links_to_other_rolls = filter(lambda a: a['href'].startswith(u'ROLL_'),
                                      soup.findAll(name='a'))
        self.debug('%d found...' % len(links_to_other_rolls))
        for link in links_to_other_rolls:
            to_return = self.get_rolls(base_dict=to_return,
                                       url_tail=link['href'])
        return to_return
