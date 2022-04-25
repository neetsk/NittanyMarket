from flask import Flask, render_template, request, session
import sqlite3 as sql
from populateDatabase import populate
import hashlib
import secrets

# Populates Database with starting data
populate()

app = Flask(__name__)
#app.config["SESSION_PERMANENT"] = False
#app.config["SECRET_KEY"] = secrets.token_urlsafe(16) 

host = 'http://127.0.0.1:5000/'

con = sql.connect("NittanyMarket.db")

#resources: sessions: https://testdriven.io/blog/flask-sessions/

#RUN APPLICATION inside | lines || & C:/Python310/python.exe c:/Users/minij/Desktop/NittanyMarket/NittanyMarket.py||

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


#@app.route('/profile/<username>, methods=['GET','POST']')
@app.route('/profile', methods=['GET', 'POST'])
def index3():
    #if user not logged in send them to login
    
    #else display user profile
    
    #fetch profile data
    
    data = fetch_profile_data()
    if request.method == 'GET':
        test = None
    else:
        #if it worked
        changePassAttempt = True
        #if change failed
        #changePassAttempt = False
    #pass data under return
    
    return render_template('profile.html', data=data, changePassAttempt=changePassAttempt)


def fetch_profile_data():
    tempUser = 'arubertelli0@nsu.edu'
    #tempPass = hashlib.sha256('TbIF16hoUqGl'.encode('utf-8')).hexdigest()
    connection = sql.connect('NittanyMarket.db')
    
    string = "SELECT * FROM Buyers WHERE email=?"
    cursor = connection.execute(string, [tempUser])
    tempdata = cursor.fetchone()
    # example result ('arubertelli0@nsu.edu', 'Ileana', 'Ziehms', 'Female', 49, 
    # 'bbeb14f144684b76b5322bdee24f8c76', '63f97e32f7894bd0bc43d113a431cb9b')

    string = "SELECT zipcode, street_num, street_name FROM Address WHERE address_id=?"
    cursor = connection.execute(string, [tempdata[5]])
    temphomeadd = cursor.fetchone()

    cursor = connection.execute(string, [tempdata[6]])
    tempbillingadd = cursor.fetchone()

    string = "SELECT SUBSTRING(credit_card_num, 16, 4) FROM Credit_Cards WHERE Owner_email=?"
    cursor = connection.execute(string, [tempUser])
    lastfourdigit = cursor.fetchone()

    return tempdata + temphomeadd + tempbillingadd + lastfourdigit


def valid_login(user, password):
    connection = sql.connect('NittanyMarket.db')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [user, password])
    return cursor.fetchone()


if __name__ == "__main__":
    app.run()

