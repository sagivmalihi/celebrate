import urllib2
import re
import itertools
import functools
import datetime
from unicodedata import normalize
from BeautifulSoup import BeautifulSoup
from celebrate import Event, db

WIKIPEDIA_HOSTNAME = "http://en.wikipedia.org"
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def parse_day(rdate):
    try:
        day_str = rdate.strftime("%b_{}").format(rdate.day)
        http_response = urllib2.urlopen("http://en.wikipedia.org/wiki/{}".format(day_str))
        page = BeautifulSoup(http_response.read())
        holidays = page.body.find('span', attrs={'id': "Holidays_and_observances"})
        all_until_next_section = itertools.takewhile(lambda t: not (getattr(t, 'name', None) == 'h2'), holidays.nextGenerator())
        events = itertools.ifilter(lambda x: getattr(x, 'name', None) == 'li', all_until_next_section)
        return events
    except:
        return []

def parse_event(rdate, event):
    try:
        return Event(event_id = 'wikipedia-' + rdate.strftime("%Y-%m-%d") + slugify(event.text), 
                     description = event.text,
                     url = WIKIPEDIA_HOSTNAME + event.a['href'],
                     rdate = rdate)
    except:
        return None
    
def scrap_wikipedia():
    date = datetime.date(2014, 1, 1)
    while date.year == 2014:
        if Event.query.filter_by(rdate=date).count() == 0:
            events = map(functools.partial(parse_event, date), parse_day(date))
            for event in filter(lambda x: x is not None, events):
                print event
                db.session.add(event)
            db.session.commit()
        
        date = date + datetime.timedelta(days=1)

if __name__ == '__main__':
    scrap_wikipedia()
