import flask
import argparse
import random
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import redirect, url_for, send_from_directory
from flask import request
import dateutil.parser
import foursquare

DEFAULT_FOURSQUARE_SEARCH_RADIUS = 2000

app = Flask(__name__)
app.config.from_object('config.defaults')
app.config.from_object('config.current')

db = SQLAlchemy(app)
foursquare_client = foursquare.Foursquare(client_id=app.config['FOURSQUARE_CLIENT_ID'], 
                                          client_secret=app.config['FOURSQUARE_CLIENT_SECRET'], 
                                          # redirect_uri='http://fondu.com/oauth/authorize',
                                          )

def parse_isodate(date):
    return dateutil.parser.parse(date).date()

class Event(db.Model):
    event_id = db.Column(db.String(80), primary_key=True)
    rdate = db.Column(db.Date)
    description = db.Column(db.String(1000))
    url = db.Column(db.String(2000))
    affiliation = db.Column(db.String(1000), default='')

    def __init__(self, event_id, rdate, description, url, affiliation=''):
        self.event_id = event_id
        self.rdate = rdate
        self.description = description 
        self.url = url
        self.affiliation = affiliation
    
    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()

    def to_dict(self):
        return dict(event_id=self.event_id,
                    rdate=self.rdate.isoformat(),
                    description=self.description,
                    url=self.url,
                    affiliation=self.affiliation,
                    )

    @classmethod
    def from_dict(cls, event_id, rdate, description, url, affiliation):
        return cls(event_id=event_id,
                   rdate=parse_isodate(rdate),
                   description=description,
                   url=url,
                   affiliation=affiliation,
                   )

    def __repr__(self):
        return '<Event {}>'.format(self.event_id)

NoEvent = lambda rdate: Event(event_id='empty-event', rdate=rdate, description="Nothing!", url="http://en.wikipedia.org/wiki/Nothing")

def generate_foursquare_link(venue):
    FOURSQUARE_LINK_TEMPLATE = u"https://foursquare.com/v/{name}/{id}"
    name = venue['name'].lower().replace(' ','-')
    id = venue['id']
    return FOURSQUARE_LINK_TEMPLATE.format(name=name, id=id)

def get_foursquare_suggestion(location):
    loc_string = "%2.2f,%2.2f" % tuple(location)
    suggestions = foursquare_client.venues.search(params=dict(query='coffee', ll=loc_string, intent='browse', radius=DEFAULT_FOURSQUARE_SEARCH_RADIUS))
    try:
        suggestion = random.choice(suggestions['venues'])
    except Exception:
        return {}
    else:
        name = suggestion['name']
        foursquare_link = generate_foursquare_link(suggestion)
        return dict(name=name, link=foursquare_link)

@app.route("/day/<date>")
def get_date(date):
    dateobj = parse_isodate(date)
    try:
        e = random.choice(Event.query.filter_by(rdate=dateobj).all())
    except IndexError:
        e = NoEvent(dateobj)
    response = e.to_dict()
    
    location = map(float, (request.args['loc[coords][latitude]'], request.args['loc[coords][longitude]']))
    response['loc'] = location
    suggestion = get_foursquare_suggestion(location)
    response['foursquare'] = suggestion
    return flask.jsonify(response)

@app.route('/static/<path:filename>')
def send_foo(filename):
     return send_from_directory('./static/', filename)

@app.route("/")
def static_index():
    return redirect(url_for('static', filename='index.html'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-db', action='store_true', default=False)
    args = parser.parse_args()
    if args.create_db:
        db.create_all()
    else:
        app.run(app.config['HOST'], app.config['PORT'])

if __name__ == "__main__":
    main()
