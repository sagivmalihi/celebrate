import flask
from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)

app.config.from_object('config')
app.config['MYSQL_DATABASE_HOST'] = '182.50.133.140'
app.config['MYSQL_DATABASE_USER'] = 'brendror'
app.config['MYSQL_DATABASE_DB'] = 'brendror'
app.config['DEBUG'] = True

mysql = MySQL()
mysql.init_app(app)

def get_cursor():
    return mysql.get_db().cursor()


@app.route("/day")
def hello():
    cursor = get_cursor()
    cursor.execute("select event_id, description, url from events where rdate='2014-01-01';")
    rows = cursor.fetchall()
    return flask.jsonify(response=rows)

if __name__ == "__main__":
    app.run()

