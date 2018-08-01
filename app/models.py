"""
app/models.py
contains models for the app
"""
import datetime
import psycopg2
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify

from app.db import Connection
conn = Connection()
class Entry(object):
    """Add new entry"""
    # constructor
    def __init__(self):
        # all entries placeholder
        self.entries = []
        self.db = conn.db_return()
    def add_entry(self, title, description, current_user):
        """Adds new entries"""

        if description and title:
            now = datetime.datetime.now()
            date_created = now.strftime("%Y-%m-%d %H:%M")
            owner_id = current_user

            cur = self.db.cursor()
            query = "INSERT INTO entries (title, date_created, description, owner_id) VALUES (%s, %s, %s, %s)"
            data = (title, date_created, description, owner_id)
            cur.execute(query, data)
            self.db.commit()
            # return true
            return True

    # def return_single_entry(self, current_user, id_entry):
    #     """ returns a single entry """
        

    # def edit_entry(self, current_user, id_entry, description, title):
    #     """  edits an entry   """

def token_required(func):
    """ decorated function for toke required """
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
    """ Handle user """

    def register_user(self, username, user_email, user_password):
        """ registers a  new user"""
        self.db = conn.db_return()
        checker = self.db.cursor()
        checker.execute("SELECT username, email FROM users")
        for user in checker.fetchall():
            if username == user[0]:
                return {"status": "fail", "message" : "user exists"}, 409

        cur = self.db.cursor()
        query = "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
        hashed_password = generate_password_hash(user_password, method='sha256')
        data = (user_email, hashed_password, username)
        cur.execute(query, data)
        self.db.commit()

    def check_existense(self, username, user_email, user_password):
        """ check if a user exists """
        

    # def search_user(self, user_email):
    #     self.db = conn.db_return()
    #     checker = self.db.cursor()
    #     checker.execute("SELECT * FROM users")
    #     found_user = [user for user in checker.fetchall() if user[2] == user_email]
    #     return found_user

    