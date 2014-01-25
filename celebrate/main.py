#!venv/bin/python
import argparse
from celebrate import app, db

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
