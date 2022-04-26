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

#RUN APPLICATION inside | lines || & C:/Python310/python.exe c:/Users/minij/Desktop/NittanyMarket/NittanyMarket.py||

#TEST LOGIN
#User: arubertelli0@nsu.edu
#Pass: 123

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

    # If we are logged in, redirect to user's profile
    if "username" in session:
        return redirect(url_for('userProfile'))

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


'''Redirects to Login if not logged in or renders the Profile page o.w.'''
@app.route('/profile', methods=['GET', 'POST'])
def userProfile():
    error = None
    # If we are not logged in, redirect to the login page
    if "username" not in session:
        return redirect(url_for('login'))
    
    # Fetch data for the user in the session
    data = fetch_profile_data(session["username"]) 

    if request.method == 'GET':
        return render_template('profile.html', data=data, changePassAttempt=False, attemptSuccess=None)
    # Method is a POST so we attempt to change the password
    else:
        attemptSuccess = valid_password_change(request.form['currentpassword'], request.form['newpassword'], request.form['newpasswordretype'])
        return render_template('profile.html', data=data, changePassAttempt=True, attemptSuccess=attemptSuccess)


'''Redirects to login page if already logged out or successfully logs out o.w.'''
@app.route('/logout')
def logout():
    # If we are not logged in, redirect to the login page
    if "username" not in session:
        return redirect(url_for('login'))

    # Once logged out, remove the user from the session
    session.pop("username", None)
    #we should instead display logout complete
    return redirect(url_for('index'))


'''Fetch user profile data for display on the profile page'''
def fetch_profile_data(user):
    connection = sql.connect('NittanyMarket.db')
    
    string = "SELECT * FROM Buyers WHERE email=?"
    cursor = connection.execute(string, [user])
    personalData = cursor.fetchone()

    string = "SELECT zipcode, street_num, street_name FROM Address WHERE address_id=?"
    cursor = connection.execute(string, [personalData[5]])
    homeAddressData = cursor.fetchone()

    cursor = connection.execute(string, [personalData[6]])
    billingAddressData = cursor.fetchone()

    string = "SELECT SUBSTRING(credit_card_num, 16, 4) FROM Credit_Cards WHERE Owner_email=?"
    cursor = connection.execute(string, [user])
    lastFourDigit = cursor.fetchone()

    return personalData + homeAddressData + billingAddressData + lastFourDigit


'''Validate login by querying the database'''
def valid_login(user, password):
    connection = sql.connect('NittanyMarket.db')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [user, password])
    return cursor.fetchone()


'''Validate Changed Password by quering the database'''
def valid_password_change(currentPassword, newPassword, newPasswordRetype):
    connection = sql.connect('NittanyMarket.db')

    if currentPassword == '':
        return 'Enter the current password'
    if newPassword == '':
        return 'Enter the new password'
    if newPasswordRetype == '':
        return 'Reenter the new password'

    if newPassword != newPasswordRetype:
        return 'Passwords do not match'
    
    hashedCurrentPass = hashlib.sha256(currentPassword.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [session['username'], hashedCurrentPass])

    if cursor.fetchone()[0] == 1:
        hashedNewPass = hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
        string = "UPDATE Users SET password=? WHERE email=? AND password=?"
        cursor = connection.execute(string, [hashedNewPass, session['username'], hashedCurrentPass])
        connection.commit()
        return 'Password successfully updated'
    else:
        return 'Incorrect password entered'


if __name__ == "__main__":
    app.run()
