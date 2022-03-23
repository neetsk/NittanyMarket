import sqlite3 as sql

def populate():
    con = sql.connect("NittanyMarket.db")

    alphabet = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']
    digits = ['0123456789']

    '''Drop Tables'''
    # Drop Tables for testing purposes
    con.execute('''DROP TABLE IF EXISTS Users''')
    con.execute('''DROP TABLE IF EXISTS Buyers''')

    con.execute('''DROP TABLE IF EXISTS Credit_Cards''')
    con.execute('''DROP TABLE IF EXISTS Address''')

    con.execute('''DROP TABLE IF EXISTS Zipcode_Info''')
    con.execute('''DROP TABLE IF EXISTS Sellers''')

    con.execute('''DROP TABLE IF EXISTS Local_Vendors''')
    con.execute('''DROP TABLE IF EXISTS Categories''')

    con.execute('''DROP TABLE IF EXISTS Product_Listings''')
    con.execute('''DROP TABLE IF EXISTS Orders''')

    con.execute('''DROP TABLE IF EXISTS Reviews''')
    con.execute('''DROP TABLE IF EXISTS Rating''')

    '''Create Tables'''
    # Users Table
    con.execute('''CREATE TABLE IF NOT EXISTS Users
        (email TEXT NOT NULL, 
        password TEXT NOT NULL,
        PRIMARY KEY (email))''')

    # Buyers Table
    con.execute('''CREATE TABLE IF NOT EXISTS Buyers
        (email TEXT NOT NULL, 
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL,
        home_address_ID TEXT NOT NULL,
        billing_address_ID TEXT NOT NULL,
        FOREIGN KEY (email) REFERENCES Users (email),
        FOREIGN KEY (home_address_ID) REFERENCES Address (address_ID),
        FOREIGN KEY (billing_address_ID) REFERENCES Address (address_ID))''')
  
    # Credit_Cards Table
    con.execute('''CREATE TABLE IF NOT EXISTS Credit_Cards
        (credit_card_num TEXT NOT NULL,
        card_code INTEGER NOT NULL,
        expire_month INTEGER NOT NULL,
        expire_year INTEGER NOT NULL,
        card_type TEXT NOT NULL,
        Owner_email TEXT NOT NULL,
        PRIMARY KEY (credit_card_num))''')

    # Address Table
    con.execute('''CREATE TABLE IF NOT EXISTS Address
        (address_ID TEXT NOT NULL,
        zipcode INTEGER NOT NULL,
        street_num INTEGER NOT NULL,
        street_name TEXT NOT NULL,
        PRIMARY KEY (address_ID))''')

    # Zipcode_Info Table
    con.execute('''CREATE TABLE IF NOT EXISTS Zipcode_Info
        (zipcode INTEGER NOT NULL,
        city TEXT NOT NULL,
        state_id CHARACTER(2) NOT NULL,
        population INTEGER NOT NULL,
        density REAL NOT NULL,
        county_name TEXT NOT NULL,
        timezone TEXT NOT NULL,
        PRIMARY KEY (zipcode))''')

    # Sellers Table
    con.execute('''CREATE TABLE IF NOT EXISTS Sellers
        (email TEXT NOT NULL,
        routing_number TEXT NOT NULL,
        account_number TEXT NOT NULL,
        balance INTEGER NOT NULL,
        FOREIGN KEY (email) REFERENCES Users (email))''')
    
    # Local_vendors Table
    con.execute('''CREATE TABLE IF NOT EXISTS Local_Vendors
        (email TEXT NOT NULL,
        business_name TEXT NOT NULL,
        business_address_ID TEXT NOT NULL,
        customer_service_number CHARACTERS(12) NOT NULL,
        FOREIGN KEY (email) REFERENCES Users (email),
        FOREIGN KEY (business_address_ID) REFERENCES Address (address_ID))''')

    # Categories Table
    con.execute('''CREATE TABLE IF NOT EXISTS Categories
        (parent_category TEXT UNIQUE NOT NULL,
        category_name TEXT NOT NULL,
        PRIMARY KEY (category_name))''')

    # Product_Listings Table
    con.execute('''CREATE TABLE IF NOT EXISTS Product_Listings
        (seller_email TEXT NOT NULL,
        listing_ID INTEGER NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        product_name TEXT NOT NULL,
        product_description TEXT NOT NULL,
        price TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (seller_email, listing_ID))''')

    # Orders Table
    con.execute('''CREATE TABLE IF NOT EXISTS Orders
        (transaction_ID INTEGER NOT NULL,
        seller_email TEXT NOT NULL,
        listing_ID INTEGER NOT NULL,
        buyer_email TEXT NOT NULL,
        date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        payment INTEGER NOT NULL,
        PRIMARY KEY (transaction_ID))''')

    # Reviews Table
    con.execute('''CREATE TABLE IF NOT EXISTS Reviews
        (buyer_email TEXT NOT NULL,
        seller_email TEXT NOT NULL,
        listing_ID INTEGER NOT NULL,
        review_desc TEXT NOT NULL,
        PRIMARY KEY (buyer_email, seller_email, listing_ID))''')

    # Rating Table
    con.execute('''CREATE TABLE IF NOT EXISTS Rating
        (buyer_email TEXT NOT NULL,
        seller_email TEXT NOT NULL,
        date DATE NOT NULL,
        rating INTEGER NOT NULL,
        rating_desc TEXT NOT NULL,
        PRIMARY KEY (buyer_email, seller_email, date))''')

    '''Populate Tables'''
    # Populate Users Table

    # Populate Buyers Table

    # Populate Credit_Cards Table

    # Populate Address Table

    # Populate Zipcode_Info Table

    # Populate Sellers Table

    # Populate Local_Vendors Table

    # Populate Categories Table

    # Populate Product_Listings Table

    # Populate Orders Table

    # Populate Reviews Table

    # Populate Rating Table