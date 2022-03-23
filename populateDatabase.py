import sqlite3 as sql
import csv

def populate():
    con = sql.connect("NittanyMarket.db")

    cur = con.cursor()

    alphabet = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']
    digits = ['0123456789']

    '''Drop Tables'''
    # Drop Tables for testing purposes
    cur.execute('''DROP TABLE IF EXISTS Users''')
    cur.execute('''DROP TABLE IF EXISTS Buyers''')

    cur.execute('''DROP TABLE IF EXISTS Credit_Cards''')
    cur.execute('''DROP TABLE IF EXISTS Address''')

    cur.execute('''DROP TABLE IF EXISTS Zipcode_Info''')
    cur.execute('''DROP TABLE IF EXISTS Sellers''')

    cur.execute('''DROP TABLE IF EXISTS Local_Vendors''')
    cur.execute('''DROP TABLE IF EXISTS Categories''')

    cur.execute('''DROP TABLE IF EXISTS Product_Listings''')
    cur.execute('''DROP TABLE IF EXISTS Orders''')

    cur.execute('''DROP TABLE IF EXISTS Reviews''')
    cur.execute('''DROP TABLE IF EXISTS Ratings''')

    '''Create Tables'''
    # Users Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Users
        (email TEXT NOT NULL, 
        password TEXT NOT NULL,
        PRIMARY KEY (email))''')

    # Buyers Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Buyers
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
    cur.execute('''CREATE TABLE IF NOT EXISTS Credit_Cards
        (credit_card_num TEXT NOT NULL,
        card_code INTEGER NOT NULL,
        expire_month INTEGER NOT NULL,
        expire_year INTEGER NOT NULL,
        card_type TEXT NOT NULL,
        Owner_email TEXT NOT NULL,
        PRIMARY KEY (credit_card_num))''')

    # Address Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Address
        (address_ID TEXT NOT NULL,
        zipcode INTEGER NOT NULL,
        street_num INTEGER NOT NULL,
        street_name TEXT NOT NULL,
        PRIMARY KEY (address_ID))''')

    # Zipcode_Info Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Zipcode_Info
        (zipcode INTEGER NOT NULL,
        city TEXT NOT NULL,
        state_id CHARACTER(2) NOT NULL,
        population INTEGER NOT NULL,
        density REAL NOT NULL,
        county_name TEXT NOT NULL,
        timezone TEXT NOT NULL,
        PRIMARY KEY (zipcode))''')

    # Sellers Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Sellers
        (email TEXT NOT NULL,
        routing_number TEXT NOT NULL,
        account_number TEXT NOT NULL,
        balance INTEGER NOT NULL,
        FOREIGN KEY (email) REFERENCES Users (email))''')
    
    # Local_vendors Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Local_Vendors
        (email TEXT NOT NULL,
        business_name TEXT NOT NULL,
        business_address_ID TEXT NOT NULL,
        customer_service_number CHARACTERS(12) NOT NULL,
        FOREIGN KEY (email) REFERENCES Users (email),
        FOREIGN KEY (business_address_ID) REFERENCES Address (address_ID))''')

    # Categories Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Categories
        (parent_category TEXT NOT NULL,
        category_name TEXT UNIQUE NOT NULL,
        PRIMARY KEY (category_name))''')

    # Product_Listings Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Product_Listings
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
    cur.execute('''CREATE TABLE IF NOT EXISTS Orders
        (transaction_ID INTEGER NOT NULL,
        seller_email TEXT NOT NULL,
        listing_ID INTEGER NOT NULL,
        buyer_email TEXT NOT NULL,
        date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        payment INTEGER NOT NULL,
        PRIMARY KEY (transaction_ID))''')

    # Reviews Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Reviews
        (buyer_email TEXT NOT NULL,
        seller_email TEXT NOT NULL,
        listing_ID INTEGER NOT NULL,
        review_desc TEXT NOT NULL,
        PRIMARY KEY (buyer_email, seller_email, listing_ID))''')

    # Rating Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Ratings
        (buyer_email TEXT NOT NULL,
        seller_email TEXT NOT NULL,
        date DATE NOT NULL,
        rating INTEGER NOT NULL,
        rating_desc TEXT NOT NULL,
        PRIMARY KEY (buyer_email, seller_email, date))''')

    '''Populate Tables'''
    insert_users = "INSERT INTO Users (email, password) VALUES (?,?)"
    insert_buyers = "INSERT INTO Buyers (email, first_name, last_name, gender, age, home_address_ID, billing_address_ID) VALUES (?,?,?,?,?,?,?)"
    insert_credit_cards = "INSERT INTO Credit_Cards (credit_card_num, card_code, expire_month, expire_year, card_type, Owner_email) VALUES (?,?,?,?,?,?)"
    insert_address = "INSERT INTO Address (address_ID, zipcode, street_num, street_name) VALUES (?,?,?,?)"
    insert_zipcode_info = "INSERT INTO Zipcode_Info (zipcode, city, state_id, population, density, county_name, timezone) VALUES (?,?,?,?,?,?,?)"
    insert_sellers = "INSERT INTO Sellers (email, routing_number, account_number, balance) VALUES (?,?,?,?)"
    insert_local_vendors = "INSERT INTO Local_Vendors (email, business_name, business_address_ID, customer_service_number) VALUES (?,?,?,?)"
    insert_categories = "INSERT INTO Categories (parent_category, category_name) VALUES (?,?)"
    insert_product_listings = "INSERT INTO Product_Listings (seller_email, listing_ID, category, title, product_name, product_description, price, quantity) VALUES (?,?,?,?,?,?,?,?)"
    insert_orders = "INSERT INTO Orders (transaction_ID, seller_email, listing_ID, buyer_email, date, quantity, payment) VALUES (?,?,?,?,?,?,?)"
    insert_reviews = "INSERT INTO Reviews (buyer_email, seller_email, listing_ID, review_desc) VALUES (?,?,?,?)"
    insert_ratings = "INSERT INTO Ratings (buyer_email, seller_email, date, rating, rating_desc) VALUES (?,?,?,?,?)"
    
    # Populate Users Table
    file = open('NittanyMarketDataset-Final/Users.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_users, contents)

    # Populate Buyers Table
    file = open('NittanyMarketDataset-Final/Buyers.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_buyers, contents)
    
    # Populate Credit_Cards Table
    file = open('NittanyMarketDataset-Final/Credit_Cards.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_credit_cards, contents)

    # Populate Address Table
    file = open('NittanyMarketDataset-Final/Address.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_address, contents)

    # Populate Zipcode_Info Table
    file = open('NittanyMarketDataset-Final/Zipcode_Info.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_zipcode_info, contents)

    # Populate Sellers Table
    file = open('NittanyMarketDataset-Final/Sellers.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_sellers, contents)

    # Populate Local_Vendors Table
    file = open('NittanyMarketDataset-Final/Local_Vendors.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_local_vendors, contents)

    # Populate Categories Table
    file = open('NittanyMarketDataset-Final/Categories.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_categories, contents)

    # Populate Product_Listings Table
    file = open('NittanyMarketDataset-Final/Product_Listing.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_product_listings, contents)

    # Populate Orders Table
    file = open('NittanyMarketDataset-Final/Orders.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_orders, contents)

    # Populate Reviews Table
    file = open('NittanyMarketDataset-Final/Reviews.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_reviews, contents)

    # Populate Rating Table
    file = open('NittanyMarketDataset-Final/Ratings.csv')
    contents = list(csv.reader(file))
    contents = contents[1:]
    cur.executemany(insert_ratings, contents)

    cur.close()
    con.commit()