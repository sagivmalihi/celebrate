import csv
import sys
from celebrate import Event, db

def decode_dict(d):
    return {k: v.decode('utf-8') if isinstance(v, basestring) else v for k,v in d.iteritems()}

def read_csv(filename):
    with open(filename, 'r') as fileobj:
        reader = csv.DictReader(fileobj, Event.get_columns())
        reader.next() # skip header
        Event.query.delete()
        for event_row in reader:
            event = Event.from_dict(**decode_dict(event_row))
            db.session.add(event)
    db.session.commit()

def main():
    filename = sys.argv[1]
    read_csv(filename)

if __name__=='__main__':
    main()
