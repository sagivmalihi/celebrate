from datetime import date
from celebrate import Event, db

events=[
    Event(event_id='new-year', rdate=date(2014, 1, 1), description="New Year's Day", url="http://en.wikipedia.org/wiki/New_Year"),
    ]

for event in events:
    db.session.add(event)
db.session.commit()
