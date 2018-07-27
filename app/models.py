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

class Entry(object):
    """Add new entry"""
    # constructor
    def __init__(self):
        # all entries placeholder
        self.entries = []
        # HOSTNAME = 'localhost'
        # USERNAME = 'postgres'
        # PASSWORD = '2grateful'
        # DATABASE = 'thriller'
        HOSTNAME = 'ec2-107-22-169-45.compute-1.amazonaws.com'
        USERNAME = 'xqvzxugpqzozsl'
        PASSWORD = '6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494'
        DATABASE = 'dbmjf8qhfukq3i'
        self.db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE, port=5432)
        # db = 'postgres://xqvzxugpqzozsl:6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494@ec2-107-22-169-45.compute-1.amazonaws.com:5432/dbmjf8qhfukq3i'

        # cur = db.cursor()
        # cur.execute("CREATE TABLE users (ID serial PRIMARY KEY, username VARCHAR (255) NOT NULL, email VARCHAR (255) NOT NULL, password VARCHAR (255));")
        # cur.execute("CREATE TABLE entries (ID serial PRIMARY KEY, title VARCHAR (255) NOT NULL, date_created VARCHAR (255) NOT NULL, description VARCHAR (255) NOT NULL, owner_id integer NOT NULL, CONSTRAINT users_id_fkey FOREIGN KEY (id)REFERENCES users (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION);")
    def add_entry(self, title, description, current_user):
        """Adds new entries"""

        if description and title:
            now = datetime.datetime.now()
            date_created = now.strftime("%Y-%m-%d %H:%M")

            # entry id
            entry_id = 1
            for i in self.entries:
                entry_id += 1
                if i['id'] == entry_id:
                    entry_id += 1
            # single_entry_holder = dict()
            # single_entry_holder['id'] = entry_id
            # single_entry_holder['title'] = title
            # single_entry_holder['description'] = description
            # single_entry_holder['created'] = str(date_created)
            # self.entries.append(single_entry_holder)
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

class User:
    """ returns available users """
    def all_the_users(self):
        """Returns all users in databse """
        # HOSTNAME = 'localhost'
        # USERNAME = 'postgres'
        # PASSWORD = '2grateful'
        # DATABASE = 'thriller'
        HOSTNAME = 'ec2-107-22-169-45.compute-1.amazonaws.com'
        USERNAME = 'xqvzxugpqzozsl'
        PASSWORD = '6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494'
        DATABASE = 'dbmjf8qhfukq3i'
        db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE, port=5432)
        # db = 'postgres://xqvzxugpqzozsl:6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494@ec2-107-22-169-45.compute-1.amazonaws.com:5432/dbmjf8qhfukq3i'
        cur = db.cursor()
        cur.execute("SELECT id, username, email, password FROM users")
        return cur.fetchall()

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
    