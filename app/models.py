"""
app/models.py
contains models for the app
"""
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
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
            try:
                cur = self.db.cursor()
                query =  "INSERT INTO entries (title, date_created, description, owner_id) VALUES (%s, %s, %s, %s)"
                data = (title, date_created, description, owner_id)
                cur.execute(query, data)
                self.db.commit()
            except:
                pass

            # return true
            return 1

        # on failure to add return false
        return 0


    def all_entries(self):
        """Return available entries"""

        return self.entries

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return jsonify({'message' : 'Please provide a token', 'token' : request.headers}), 401

        try:
            data = jwt.decode(token, 'shark')
            current_user = data['user_id']
        except:
            return jsonify({'message' : 'Provided token is invalid, try again'}), 401

        return func(current_user, *args, **kwargs)

    return decorated
    