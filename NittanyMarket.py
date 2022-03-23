from flask import Flask, render_template, request
import sqlite3 as sql
from populateDatabase import populate
import hashlib

# Populates Database with starting data
populate()

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

con = sql.connect("NittanyMarket.db")


@app.route('/')
def index():
    return render_template('index.html')


#use args for get and form for post
@app.route('/logincomplete', methods=['POST', 'GET'])
def index2():
    error = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/x-www-form-urlencoded'):
        if request.method == 'POST':
            result = valid_login(request.form['userid'], request.form['password'])
            if result[0] == 1:
                return render_template('logincomplete.html')
            else:
                error = 'login failed'
    return render_template('loginfailed.html', error=error)


def valid_login(user, password):
    connection = sql.connect('NittanyMarket.db')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [user, password])
    return cursor.fetchone()

if __name__ == "__main__":
    app.run()

