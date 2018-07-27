"""
app/auth/views.py
"""
import psycopg2
import re
from flask import Blueprint, request, make_response, jsonify, session
from flask_api import FlaskAPI
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
# authentication blueprint

AUTH = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')

# from app.models import Accounts

# ACCOUNT = Accounts()
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

@AUTH.route('/', methods=['GET'])
def index():
    """
    This route welcomes a user.
    ---
    tags:
      - Thriller Diary Api
    responses:
      500:
        description: There is a server Error
      200:
        description: A welcoming message has been displayed
     """
    if request.method == 'GET':
        
        # the following is a welcoming message (at the landing page)
        welcome_message = {"Message": [{
            "Welcome":"Hey! welcome to thriller diary api"
            }]}

        response = {"status": "success", "Message": welcome_message}
        return response, 200
@AUTH.route('/signup', methods=['POST'])
def user_registration():
    user_email = request.data.get('email', '')
    user_password = request.data.get('password', '')
    username = request.data.get('username', '')

    # check for empty input
    if not user_email or not user_password or not username:
        return {"status": "fail", "Message": "Check your details and try again"}, 401
    # check username
    the_username = username.lower()
    if not re.match(r"^[a-z0-9_]*$", the_username):
        return {"status": "fail", "Message": "Invalid usernamee.Try again"}, 401
    # check password length
    if len(user_password) < 4:
        return {"status": "fail", "Message": "Too short password(at least 4 characters needed)"}, 401
    # check email validity
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", user_email):
        return {"status": "fail", "Message": "Invalid email.Try again"}, 401
    # check user existense
    checker = db.cursor()
    checker.execute("SELECT username, email FROM users")
    for user in checker.fetchall():
        if username == user[0]:
            return {"status": "fail", "message" : "user exists"}, 409

    cur = db.cursor()
    query =  "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
    hashed_password = generate_password_hash(user_password, method='sha256')
    data = (user_email, hashed_password, username)
    cur.execute(query, data)
    db.commit()
    # ACCOUNT.register_user(email, password)
    response = {"status": "success", "Registered": {"Email":str(user_email), "Username":str(username)}}
    return response, 201

# @AUTH.route('/users', methods=['GET'])
# def all_users():
#     response = {"status": "success", "users": ACCOUNT.all_users()}
#     return response, 200

@AUTH.route('/login', methods=['POST'])
def login():
    user_email = str(request.data.get('email', '').strip())
    user_password = str(request.data.get('password', '').strip())
    # check if the submited data
    if not user_email or not user_password:
        return {"status": "fail", "Message": "Check your details and try again"}, 401
    # check user existense
    checker = db.cursor()
    checker.execute("SELECT id, username, email, password FROM users")
    for user in checker.fetchall():
        if user_email == user[2]:
            if check_password_hash(user[3], user_password):
                
                token = jwt.encode({'user_id' : user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'shark')
                return jsonify({'token' : token.decode('UTF-8')})
                # session["pulic_id"] = user[0]
                # return {"status": "success", "Message": "Login successful"}, 200
            return {"status":"fail", "message":"Oops! check your details and try again"}, 401
