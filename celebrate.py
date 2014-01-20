import flask
import argparse
import random
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import redirect, url_for, send_from_directory
import dateutil.parser

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

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

@app.route("/day/<date>")
def get_date(date):
    dateobj = parse_isodate(date)
    try:
        e = random.choice(Event.query.filter_by(rdate=dateobj).all())
    except IndexError:
        e = NoEvent(dateobj)
    return flask.jsonify(e.to_dict())

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
