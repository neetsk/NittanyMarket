from flask import Flask, render_template, request
import sqlite3 as sql
from populateDatabase import populate
import hashlib

# Populates Database with starting data
populate()

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

con = sql.connect("NittanyMarket.db")

#TEST LOGIN
#User: arubertelli0@nsu.edu
#Pass: TbIF16hoUqGl


@app.route('/')
def index():
    return render_template('index.html')


#use args for get and form for post
@app.route('/logincomplete', methods=['POST', 'GET'])
def index2():
    error = None
    content_type = request.headers.get('Content-Type') #content type check to see if its normal one sent vs json
    if (content_type == 'application/x-www-form-urlencoded'):
        if request.method == 'POST':
            result = valid_login(request.form['userid'], request.form['password']) #calls valid login
            if result[0] == 1: #if we have a user and pass that match, successfully login
                #return render_template('logincomplete.html')
                return render_template('profile.html')
            else:
                error = 'login failed'
    return render_template('loginfailed.html', error=error) #we didnt have a password and user that match so we fail login with error=loginfailed


@app.route('/profile', methods=['GET'])
def index3():
    #if user not logged in send them to login
    if (False):
        None=None
    #else display user profile
    else: 
        #fetch profile data
        data = fetch_profile_data()
        #pass data under return
    return render_template('profile.html', data=data)


def fetch_profile_data():
    return True


def valid_login(user, password):
    connection = sql.connect('NittanyMarket.db')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [user, password])
    return cursor.fetchone()


if __name__ == "__main__":
    app.run()

