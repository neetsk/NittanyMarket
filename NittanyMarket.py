from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3 as sql
from populateDatabase import populate
import hashlib

# Populates Database with starting data
populate()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = "7c90dc90568ad551eb574e4b7a3d86ab08ab771351d6fa858fb2d7ec308d63b4"

host = 'http://127.0.0.1:5000/'

con = sql.connect("NittanyMarket.db")

#RUN APPLICATION inside | lines || & C:/Python310/python.exe c:/Users/minij/Desktop/NittanyMarket/NittanyMarket.py||

#TEST LOGIN
#User: arubertelli0@nsu.edu
#Pass: TbIF16hoUqGl

'''Redirects to Profile if logged in or Login o.w.'''
@app.route('/')
def index():
    # If we are logged in, redirect to user's profile
    if "username" in session:
        return redirect(url_for('userProfile'))

    # If we are not logged in, redirect to the login page
    return redirect(url_for('login'))


'''Redirects to Profile if logged in or renders the Login page o.w.'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    # If our method is a GET request, render the login page
    # If our method is a POST request, validate the login
    if request.method == 'GET': 
        return render_template('login.html')
    else:
        result = valid_login(request.form['userid'], request.form['password']) # determines valid login in valid_login function
        if result[0] == 1: #if we have a user and pass that match, successfully login
            session["username"] = request.form['userid'] #adds user to session
            return redirect(url_for('userProfile'))
        else:
            error = 'login failed'
    return render_template('loginfailed.html', error=error)


#@app.route('/profile/<username>, methods=['GET','POST']')
'''Redirects to Login if not logged in or renders the Profile page o.w.'''
@app.route('/profile', methods=['GET', 'POST'])
def userProfile():
    # If we are not logged in, redirect to the login page
    if "username" not in session:
        return redirect(url_for('login'))
    
    # Fetch data for the user in the session
    data = fetch_profile_data(session["username"]) 

    if request.method == 'GET':
        #render webpage
        test = None
    else:
        #post method means attempted password change
        #if it worked
        changePassAttempt = True
        #if change failed
        #changePassAttempt = False
    #pass data under return
    
    return render_template('profile.html', data=data, changePassAttempt=changePassAttempt)

@app.route('/logout')
def logout():
    if "username" not in session:
        return redirect(url_for('login'))

    session.pop("username", None)
    return redirect(url_for('index'))


def fetch_profile_data(user):
    connection = sql.connect('NittanyMarket.db')
    
    string = "SELECT * FROM Buyers WHERE email=?"
    cursor = connection.execute(string, [user])
    tempdata = cursor.fetchone()
    # example result ('arubertelli0@nsu.edu', 'Ileana', 'Ziehms', 'Female', 49, 
    # 'bbeb14f144684b76b5322bdee24f8c76', '63f97e32f7894bd0bc43d113a431cb9b')

    string = "SELECT zipcode, street_num, street_name FROM Address WHERE address_id=?"
    cursor = connection.execute(string, [tempdata[5]])
    temphomeadd = cursor.fetchone()

    cursor = connection.execute(string, [tempdata[6]])
    tempbillingadd = cursor.fetchone()

    string = "SELECT SUBSTRING(credit_card_num, 16, 4) FROM Credit_Cards WHERE Owner_email=?"
    cursor = connection.execute(string, [user])
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

"""
#use args for get and form for post
@app.route('/logincomplete', methods=['POST', 'GET'])
def index2():
    if "username" in session:
        return render_template('logincomplete.html')

    error = None
    content_type = request.headers.get('Content-Type') #content type check to see if its normal one sent vs json
    if (content_type == 'application/x-www-form-urlencoded'):
        if request.method == 'POST':
            result = valid_login(request.form['userid'], request.form['password']) #calls valid login
            if result[0] == 1: #if we have a user and pass that match, successfully login
                session["username"] = request.form['userid'] #adds user to session
                return render_template('logincomplete')
                #return render_template('profile.html')
            else:
                error = 'login failed'
    return render_template('loginfailed.html', error=error) #we didnt have a password and user that match so we fail login with error=loginfailed
"""
