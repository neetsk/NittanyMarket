from email import header
from os import curdir
from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3 as sql
from populateDatabase import populate
import hashlib

'''Populates Database with starting data'''
# populate()

'''Creates a Flask app with session data saved'''
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = "7c90dc90568ad551eb574e4b7a3d86ab08ab771351d6fa858fb2d7ec308d63b4"

host = 'http://127.0.0.1:5000/'

#RUN APPLICATION: & C:/Python310/python.exe c:/Users/minij/Desktop/NittanyMarket/NittanyMarket.py

#TEST LOGIN
'''Non Seller Login'''
#User: arubertelli0@nsu.edu
#Pass: 123
'''Seller Login'''
#User: nrideoutmi@nsu.edu
#Pass: CBCA4zXar

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
        return render_template('login.html', error=error)
    else:
        result = valid_login(request.form['userid'], request.form['password']) # determines valid login in valid_login function
        if result[0] == 1: #if we have a user and pass that match, successfully login
            session["username"] = request.form['userid'] #adds user to session

            # Query if a user is a seller. If so, add that information to the session
            connection = sql.connect('NittanyMarket.db')
            string = "SELECT COUNT(1) FROM Users WHERE email=?"
            cursor = connection.execute(string, [session['username']])
            if cursor.fetchone()[0] == 1:
                session['seller'] = session['username']
            return redirect(url_for('userProfile'))
        else:
            error = 'Login Failed'
    return render_template('login.html', error=error)


'''Redirects to Login if not logged in or renders the Profile page o.w.'''
@app.route('/profile', methods=['GET', 'POST'])
def userProfile():
    error = None
    # If we are not logged in, redirect to the login page
    if "username" not in session:
        return redirect(url_for('login'))
    
    # Fetch data for the user in the session
    data = fetch_profile_data(session["username"]) 

    # Check if a user is logged in
    userLoggedIn = False
    if "username" in session:
        userLoggedIn = True

    # Check if a user is a seller
    userIsSeller = False
    if 'seller' in session:
        userIsSeller = True

    if request.method == 'GET':
        return render_template('profile.html', data=data, changePassAttempt=False, attemptSuccess=None, 
            userLoggedIn=userLoggedIn, userIsSeller=userIsSeller)
    # Method is a POST so the user attempted to change the password
    else:
        attemptSuccess = valid_password_change(request.form['currentpassword'], request.form['newpassword'], request.form['newpasswordretype'])
        return render_template('profile.html', data=data, changePassAttempt=True, attemptSuccess=attemptSuccess, 
            userLoggedIn=userLoggedIn, userIsSeller=userIsSeller)


'''Redirects to login page if already logged out or successfully logs out o.w.'''
@app.route('/logout')
def logout():
    # If we are not logged in, redirect to the login page
    if "username" not in session:
        return redirect(url_for('login'))

    # Once logged out, remove the user from the session
    session.pop("username", None)
    if 'seller' in session:
        session.pop('seller', None)
        
    return redirect(url_for('index'))


'''Shows the product listings page and adjusts features based on if a user is logged in or not and if they are a seller'''
@app.route('/productlistings', methods=['GET', 'POST'])
def productlistings():
    # Track the subCategory List to be displayed in the dropdown box as well as
    # all possible products in every subCategory's subCategories and store them
    # in the product list
    subCategoryList = []
    fullCategoryList = []
    productList = []

    # If we are just viewing the page for the first time, we display all products with 'Root'
    if request.method == 'GET':
        headCategory = 'Root'
        subCategoryList.append('Root')
        fullCategoryList.append('Root')
    if request.method == 'POST': # If we want to filter, we change the headCategory to the outermost Category
        if 'Reset' in request.form:
            headCategory = 'Root'
        else:
            headCategory = request.form['Category']
        subCategoryList.append(headCategory)
        fullCategoryList.append(headCategory)
   
    connection = sql.connect('NittanyMarket.db')
    
    # Fetch all subCategories for the headCategory
    string = "SELECT * FROM Categories WHERE parent_category=?"
    cursor = connection.execute(string, [headCategory])
    subCategory = cursor.fetchall()

    for directSubcategories in subCategory:
        subCategoryList.append(directSubcategories[1])
        fullCategoryList.append(directSubcategories[1])

    # Remove headCategory since we don't want it displaying in the drop down.
    # We also already have all of its subCategories so we don't need it repeating
    if headCategory in subCategoryList:
        subCategoryList.remove(headCategory)
        fullCategoryList.remove(headCategory)

    # Find each category's subcategories and add them to a list.
    # When iterating through the list, the new additions will be iterated through
    # as well. This makes the search recursive and completely traverses the tree
    for subCategoriesToHeadCategory in fullCategoryList:
        string = "SELECT * FROM Categories WHERE parent_category=?"
        cursor = connection.execute(string, [subCategoriesToHeadCategory])
        subCategory = cursor.fetchall()
        for newCategoriesFound in subCategory:
            fullCategoryList.append(newCategoriesFound[1])

    # Remove root from display
    if headCategory != 'Root':  
        fullCategoryList.append(headCategory)

    # Grab all products associated with the headCategory as well as
    # all subCategories found
    for category in fullCategoryList:
        string = "SELECT * FROM Product_Listings WHERE category=?"
        cursor = connection.execute(string, [category])
        queryResult = cursor.fetchall()
        
        for y in queryResult:
            productList.append(y)

    # Check if the user is in the session
    userLoggedIn = False
    if "username" in session:
        userLoggedIn = True

    # Check if the user is a seller
    userIsSeller = False
    if 'seller' in session:
        userIsSeller = True

    return render_template('productlistings.html', headCategory=headCategory, categoryList=subCategoryList, productList=productList,
        userLoggedIn=userLoggedIn, userIsSeller=userIsSeller)


'''Shows the product page information and allows buyers to purchase the product'''
@app.route('/product', methods=['GET', 'POST'])
def product():
    # Get means a product was not specified so we return to the product page
    if request.method == 'GET':
        return redirect(url_for('productlistings'))

    connection = sql.connect('NittanyMarket.db')
    
    # Find the product to display
    string = "SELECT * FROM Product_Listings WHERE Listing_ID=?"
    cursor = connection.execute(string, [request.form['View']])
    data = cursor.fetchone()

    # Check if there is a user logged in
    userLoggedIn = False
    if "username" in session:
        userLoggedIn = True

    # Check if the user is a seller
    userIsSeller = False
    if 'seller' in session:
        userIsSeller = True

    return render_template('product.html', data=data, userLoggedIn=userLoggedIn, userIsSeller=userIsSeller)


'''Allows a seller to post a product listing'''
@app.route('/publishproductlisting', methods=['GET', 'POST'])
def publishproductlisting():
    error = None
    # If we are not logged in, redirect to the login page
    if "username" not in session:
        return redirect(url_for('login'))
    
    # If we are somehow not a seller, redirect to the profile page
    if 'seller' not in session:
        return redirect(url_for('userProfile'))

    if request.method == 'POST':
        # Error checking Entries
        if request.form['category'] == '':
            error = 'Enter a Category'
        elif request.form['title'] == '':
            error = 'Enter a Title'
        elif request.form['productname'] == '':
            error = 'Enter a Product Name'
        elif request.form['productdescription'] == '':
            error = 'Enter a Product Description'
        elif request.form['price'] == '':
            error = 'Enter a Price'
        elif not request.form['price'].isdigit():
            error = 'Price Invalid'
        elif int(request.form['price']) < 1:
            error = 'Price Invalid'
        elif request.form['quantity'] == '':
            error = 'Enter a Quantity'
        elif not request.form['quantity'].isdigit():
            error = 'Quantity Invalid'
        elif int(request.form['quantity']) < 1:
            error = 'Quantity Invalid'

        connection = sql.connect('NittanyMarket.db')
        
        # Check if the email is valid
        string = "SELECT COUNT(1) FROM Users WHERE email=?"
        cursor = connection.execute(string, [session['username']])
        emailExists = cursor.fetchone()[0]
        string = "SELECT COUNT(1) FROM Sellers WHERE email=?"
        cursor = connection.execute(string, [session['username']])
        sellerExists = cursor.fetchone()[0]
        if emailExists == 0 or sellerExists == 0:
            error = 'User is not authorized'
        
        # If we have no errors, commit to the database
        if error == None:
            print('ADDING')
            # Check if the category exists
            string = "SELECT * FROM Categories WHERE category_name=?"
            cursor = connection.execute(string, [request.form['category']])
            result = cursor.fetchone()
            if result == None:
                string = '''INSERT INTO Categories (parent_category, category_name) VALUES (?,?)'''
                cursor = connection.execute(string, ['Root', request.form['category']])

            # Generating a new ID
            string = '''SELECT MAX(listing_ID) FROM Product_Listings'''
            cursor = connection.execute(string)
            maxID = cursor.fetchone()[0]

            # Inserting new Product into DB
            string = '''INSERT INTO Product_Listings (seller_email, listing_ID, category, title, 
                product_name, product_description, price, quantity) VALUES (?,?,?,?,?,?,?,?)'''
            cursor = connection.execute(string, [session['username'], maxID + 1, request.form['category'], request.form['title'], 
                request.form['productname'], request.form['productdescription'], request.form['price'], request.form['quantity']])
            
            # Commit Changes
            connection.commit()
            error='Successful'

    return render_template('publishproductlisting.html', userLoggedIn=True, userIsSeller=True, error=error)


'''Fetch user profile data for display on the profile page'''
def fetch_profile_data(user):
    connection = sql.connect('NittanyMarket.db')
    
    # Fetch user data
    string = "SELECT * FROM Buyers WHERE email=?"
    cursor = connection.execute(string, [user])
    personalData = cursor.fetchone()

    # Fetch extra address information
    string = "SELECT zipcode, street_num, street_name FROM Address WHERE address_id=?"
    cursor = connection.execute(string, [personalData[5]])
    homeAddressData = cursor.fetchone()

    cursor = connection.execute(string, [personalData[6]])
    billingAddressData = cursor.fetchone()

    # Fetch last 4 digits of credit card
    string = "SELECT SUBSTRING(credit_card_num, 16, 4) FROM Credit_Cards WHERE Owner_email=?"
    cursor = connection.execute(string, [user])
    lastFourDigit = cursor.fetchone()

    # Return all data
    return personalData + homeAddressData + billingAddressData + lastFourDigit


'''Validate login by querying the database'''
def valid_login(user, password):
    # Validate login of user by encrypting password and querying database
    connection = sql.connect('NittanyMarket.db')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [user, password])
    return cursor.fetchone()


'''Validate Changed Password by quering the database'''
def valid_password_change(currentPassword, newPassword, newPasswordRetype):
    connection = sql.connect('NittanyMarket.db')

    # Error checking Password entry
    if currentPassword == '':
        return 'Enter the current password'
    if newPassword == '':
        return 'Enter the new password'
    if newPasswordRetype == '':
        return 'Reenter the new password'

    if newPassword != newPasswordRetype:
        return 'Passwords do not match'
    
    # Confirming if current password matches
    hashedCurrentPass = hashlib.sha256(currentPassword.encode('utf-8')).hexdigest()
    string = "SELECT COUNT(1) FROM Users WHERE email=? AND password=?"
    cursor = connection.execute(string, [session['username'], hashedCurrentPass])

    # If the password matches, update database
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
