import csv
import sys
from celebrate import Event

def encode_dict(d):
    return {k: v.encode('utf-8') if isinstance(v, unicode) else v for k,v in d.iteritems()}

def write_bom(fileobj):
    fileobj.write(u'\ufeff'.encode('utf8'))

def dump_csv(fileobj=sys.stdout):
    writer = csv.DictWriter(fileobj, Event.get_columns())
    writer.writeheader()
    for event in Event.query.all():
        writer.writerow(encode_dict(event.to_dict()))

if __name__=='__main__':
    dump_csv()
