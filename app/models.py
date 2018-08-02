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
CONN = Connection()
class Entry(object):
    """Add new entry"""
    # constructor
    def __init__(self):
        # all entries placeholder
        self.entries = []
        self.db = CONN.db_return()
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

    def all_entries(self, current_user):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM entries")
        certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
        response = {"status": "success", "Entries": certain_user_entries}
        return response, 200

    def return_single_entry(self, current_user, id_entry):
        """ returns a single entry """
        cur = self.db.cursor()
        cur.execute("SELECT * FROM entries")
        certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
        entries_user = [an_entry for an_entry in certain_user_entries if an_entry[0] == id_entry]
        if len(entries_user) == 0:
            return {"status":"fail", "message":"entry unavailable"}, 404
        else:
            entry_id = entries_user[0][0]
            title = entries_user[0][1]
            date_created = entries_user[0][2]
            description = entries_user[0][3]
            response = {"status": "success", "entry": {"id":entry_id,
                                                        "title":str(title),
                                                        "description":str(description),
                                                        "created":date_created}}
            return response, 200

    def edit_entry(self, current_user, id_entry, description, title):
        """  edits an entry   """
        cur = self.db.cursor()
        cur.execute("SELECT * FROM entries")
        certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
        entries_user = [an_entry for an_entry in certain_user_entries if an_entry[0] == id_entry]
        if len(entries_user) == 0:
            return {"status":"fail", "message":"entry not found"}, 404
        for entry in certain_user_entries:
            # update the entry
            query = "UPDATE entries SET description=(%s), title=(%s) WHERE id = (%s)"
            data = (description, title, id_entry)
            cur.execute(query, data)
            self.db.commit()
            response = {
                "status": "success",
                "Updated":{"id":id_entry,"title":entries_user[0][1], "description": entries_user[0][3]}}
            return response, 201

    def delete_entry(self, current_user, id_entry):
        """ gets rid of an entry """
        cur = self.db.cursor()
        cur.execute("SELECT * FROM entries")
        certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
        entries_user = [an_entry for an_entry in certain_user_entries if an_entry[0] == id_entry]
        if len(entries_user) == 0:
            return {"status":"fail", "message":"entry not found"}, 404
        query = "DELETE from entries WHERE entries.id = (%s)"
        cur.execute(query, [id_entry])
        self.db.commit()
        response = {
            "status":"success",
            "Deleted":{"id":id_entry,"title":entries_user[0][1], "description": entries_user[0][3]}
        }
        return response, 200

def token_required(func):
    """ decorated function for toke required """
    @wraps(func)
    def decorated(*args, **kwargs):
        """ assigns a token using the user id """
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

    def __init__(self):
        self.db = CONN.db_return()

    def register_user(self, username, user_email, user_password):
        """ registers a  new user"""
        checker = self.db.cursor()
        checker.execute("SELECT username, email FROM users")
        for user in checker.fetchall():
            # if username == user[0]:
            #     return {"status": "fail", "message" : "user exists"}, 409
            if user_email == user[1]:
                return {"status": "fail", "message" : "user exists"}, 409

        cur = self.db.cursor()
        query = "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
        hashed_password = generate_password_hash(user_password, method='sha256')
        data = (user_email, hashed_password, username)
        cur.execute(query, data)
        self.db.commit()
        response = {"status": "success", 
            "Registered": {"Email":str(user_email), 
                            "Username":str(username)}}
        return response, 201
    
    def login_user(self, user_email, user_password):
        checker = self.db.cursor()
        checker.execute("SELECT * FROM users")
        found_user = [user for user in checker.fetchall() if user[2] == user_email]
        if len(found_user) == 0:
            return {"status":"fail", "message":"Oops! check your details and try again"}, 404
        elif check_password_hash(found_user[0][3], user_password):        
            token = jwt.encode({'user_id' : found_user[0][0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=300)}, 'shark')
            return jsonify({'token' : token.decode('UTF-8')}), 200  
        else:
            return {"status":"fail", "message": "Oops! check your details and try again"}, 401



    