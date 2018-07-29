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


from app.db import Connection

conn = Connection()

db = conn.db_return()

@AUTH.route('/', methods=['GET'])
def index():
    """
    This route welcomes a user.
    ---
    tags:
      - Routes
    responses:
      500:
        description: There is a server Error
      200:
        description: A welcoming message has been displayed
      403:
        description: Method is not allowed
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
    """
This is the signup route
    Call this api route passing a username, email, and password in the body to get registered at Thriller Diary Api
    ---
    tags:
      - Routes
    parameters:
      - name: body
        in: body
        required: true
        description: The signup credentials
        schema:
          type: object
          required:
            -username
            -email
            -password
          properties:
            username:
              type: string
              example: english
            email:
              type: string
              example: english@gmail.com
            password:
              type: string
              example: strongestpassword

    responses:
      500:
        description: Error There was a server error!
      201:
        description: User created successfully
      409:
        description: User with the provided email or username exists
      401:
        description: Submitted details were not accepted
      403:
        description: Method is not allowed
"""
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

@AUTH.route('/login', methods=['POST'])
def login():
    """
This is the sign-in route
    Call this api route passing a email and password to log in at Thriller Diary Api
    ---
    tags:
      - Routes
    parameters:
      - name: body
        in: body
        required: true
        description: The log in credentials
        schema:
          type: object
          required:
            -email
            -password
          properties:
            email:
              type: string
              example: english@gmail.com
            password:
              type: string
              example: strongestpassword
    responses:
      500:
        description: Error There was a server error!
      200:
        description: logged successfully(a token is given)
      401:
        description: details are not as expected
      403:
        description: Method is not allowed
    """
    user_email = str(request.data.get('email', '').strip())
    user_password = str(request.data.get('password', '').strip())
    # check if the submited data
    if not user_email or not user_password:
        return {"status": "fail", "Message": "Check your details and try again"}, 401
    # check password length
    if len(user_password) < 4:
        return {"status": "fail", "Message": "Too short password(at least 4 characters needed)"}, 401
    # check email validity
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", user_email):
        return {"status": "fail", "Message": "Invalid email.Try again"}, 401
    # check user existense
    checker = db.cursor()
    checker.execute("SELECT * FROM users")
    found_user = [user for user in checker.fetchall() if user[2] == user_email]
    if len(found_user) == 0:
          return {"status":"fail", "message":"You are not registered"}, 404
    elif check_password_hash(found_user[0][3], user_password):       
        token = jwt.encode({'user_id' : found_user[0][0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'shark')
        return jsonify({'token' : token.decode('UTF-8')}), 200     
    else:
      return {"status":"fail", "message": "Oops! check your details and try again"}, 401