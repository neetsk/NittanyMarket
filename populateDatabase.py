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
        (email TEXT, 
        password TEXT,
        PRIMARY KEY (email))''')

    # Buyers Table
    con.execute('''CREATE TABLE IF NOT EXISTS Buyers
        (email TEXT, 
        first_name TEXT, 
        last_name TEXT, 
        gender TEXT,
        age INTEGER,
        home_address_id TEXT,
        billing_address_id TEXT,
        FOREIGN KEY (email) REFERENCES Users)''')
    
    # Credit_Cards Table
    con.execute('''CREATE TABLE IF NOT EXISTS Credit_Cards
        (credit_card_num TEXT,
        card_code INTEGER,
        expire_month INTEGER,
        expire_year INTEGER,
        card_type TEXT,
        Owner_email TEXT,
        PRIMARY KEY (credit_card_num))''')

    # Address Table
    con.execute('''CREATE TABLE IF NOT EXISTS Address
        (address_ID TEXT,
        zipcode INTEGER,
        street_num INTEGER,
        street_name TEXT,
        PRIMARY KEY (address_ID))''')

    # Zipcode_Info Table
    con.execute('''CREATE TABLE IF NOT EXISTS Zipcode_Info
        (zipcode INTEGER,
        city TEXT,
        state_id CHARACTER(2),
        population INTEGER,
        density REAL,
        county_name TEXT,
        timezone TEXT,
        PRIMARY KEY (zipcode))''')

    # Sellers Table
    con.execute('''CREATE TABLE IF NOT EXISTS Sellers
        (email TEXT,
        routing_number TEXT,
        account_number TEXT,
        balance INTEGER,
        FOREIGN KEY (email) REFERENCES Users)''')
    
    # Local_vendors Table
    con.execute('''CREATE TABLE IF NOT EXISTS Local_Vendors
        (email TEXT,
        business_name TEXT,
        business_address_ID TEXT,
        customer_service_number CHARACTERS(12),
        FOREIGN KEY (email) REFERENCES Users)''')

    # Categories Table
    con.execute('''CREATE TABLE IF NOT EXISTS Categories
    (parent_category TEXT,
    category_name TEXT,
    PRIMARY KEY (category_name))''')

    # Product_Listings Table
    con.execute('''CREATE TABLE IF NOT EXISTS Product_Listings
    (seller_email TEXT,
    listing_ID INTEGER,
    category TEXT,
    title TEXT,
    product_name TEXT,
    product_description TEXT,
    price TEXT,
    quantity INTEGER,
    PRIMARY KEY (seller_email, listing_ID))''')

    # Orders Table
    con.execute('''CREATE TABLE IF NOT EXISTS Orders
    (transaction_ID INTEGER,
    seller_email TEXT,
    listing_ID INTEGER,
    buyer_email TEXT,
    date DATE,
    quantity INTEGER
    payment INTEGER,
    PRIMARY KEY (transaction_ID))''')

    # Reviews Table
    con.execute('''CREATE TABLE IF NOT EXISTS Reviews
        (buyer_email TEXT,
        seller_email TEXT,
        listing_ID INTEGER,
        review_desc TEXT,
        PRIMARY KEY (buyer_email, seller_email, listing_ID))''')

    # Rating Table
    con.execute('''CREATE TABLE IF NOT EXISTS Rating
        (buyer_email TEXT,
        seller_email TEXT,
        date DATE,
        rating INTEGER,
        rating_desc TEXT,
        PRIMARY KEY (buyer_email, seller_email, date))''')