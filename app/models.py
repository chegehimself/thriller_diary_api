"""
app/models.py
contains models for the app
"""
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import datetime
import jwt
import os
from functools import wraps
from flask import request, jsonify, current_app, session

from app.db import Connection

conn = Connection()
class Entry(object):
    """Add new entry"""
    # constructor
    def __init__(self):
        # all entries placeholder
        self.entries = []
        self.db = conn.db_return()
        # cur = db.cursor()
        # cur.execute("CREATE TABLE users (ID serial PRIMARY KEY, username VARCHAR (255) NOT NULL, email VARCHAR (255) NOT NULL, password VARCHAR (255));")
        # cur.execute("CREATE TABLE entries (ID serial PRIMARY KEY, title VARCHAR (255) NOT NULL, date_created VARCHAR (255) NOT NULL, description VARCHAR (255) NOT NULL, owner_id integer NOT NULL, CONSTRAINT users_id_fkey FOREIGN KEY (id)REFERENCES users (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION);")
    def add_entry(self, title, description, current_user):
        """Adds new entries"""

        if description and title:
            now = datetime.datetime.now()
            date_created = now.strftime("%Y-%m-%d %H:%M")
            owner_id = current_user
    
            cur = self.db.cursor()
            query =  "INSERT INTO entries (title, date_created, description, owner_id) VALUES (%s, %s, %s, %s)"
            data = (title, date_created, description, owner_id)
            cur.execute(query, data)
            self.db.commit()
            

            # return true
            return 1

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if not 'access-token' in request.headers:
            return jsonify({"status":"fail", 'message' : 'Please provide a token'}), 401
        
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        try:
            data = jwt.decode(token, 'shark')
            current_user = data['user_id']
        except:
            return jsonify({'message' : 'Provided token is invalid, try again'}), 401

        return func(current_user, *args, **kwargs)

    return decorated

class User(object): 
    # check user existense

    def register_user(self, username, user_email, user_password):
        self.db = conn.db_return()
        checker = self.db.cursor()
        checker.execute("SELECT username, email FROM users")
        for user in checker.fetchall():
            if username == user[0]:
                return {"status": "fail", "message" : "user exists"}, 409

        cur = self.db.cursor()
        query =  "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
        hashed_password = generate_password_hash(user_password, method='sha256')
        data = (user_email, hashed_password, username)
        cur.execute(query, data)
        self.db.commit()

    def login_user(self, user_email, user_password):
         # check user existense
        checker = self.db.cursor()
        checker.execute("SELECT * FROM users")
        found_user = [user for user in checker.fetchall() if user[2] == user_email]
        if len(found_user) == 0:
            return {"status":"fail", "message":"You are not registered"}, 404
        elif check_password_hash(found_user[0][3], user_password):        
            token = jwt.encode({'user_id' : found_user[0][0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=300)}, 'shark')
            return jsonify({'token' : token.decode('UTF-8')}), 200     