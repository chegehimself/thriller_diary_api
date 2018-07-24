"""
app/auth/views.py
"""
import psycopg2
import re
from flask import Blueprint, request, make_response, jsonify
from flask_api import FlaskAPI
from werkzeug.security import generate_password_hash, check_password_hash

# authentication blueprint

AUTH = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')

# from app.models import Accounts

# ACCOUNT = Accounts()
HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '2grateful'
DATABASE = 'thriller'
db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)

@AUTH.route('/', methods=['GET'])
def index():
    """ root """
    if request.method == 'GET':
        
        # the following is a welcoming message (at the landing page)
        welcome_message = {"Message": [{
            "Welcome":"Hey! welcome to thriller diary api"
            }]}

        response = {"status": "success", "Message": welcome_message}
        return response, 200
@AUTH.route('/test', methods=['GET'])
def test():
    cur = db.cursor()
    cur.execute("SELECT username, email, password FROM users")
    # for username, email in cur.fetchall():

    response = {"status": "success", "all": cur.fetchall()}
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
    response = {"status": "success", "Registered": {"Email":str(user_email), "Username":str(username), "Password":str(user_password)}}
    return response, 201

# @AUTH.route('/users', methods=['GET'])
# def all_users():
#     response = {"status": "success", "users": ACCOUNT.all_users()}
#     return response, 200

@AUTH.route('/login', methods=['POST'])
def login():
    user_email = request.data.get('email', '')
    user_password = request.data.get('password', '')
    # check if the submited data
    if not user_email or not user_password:
        return {"status": "fail", "Message": "Check your details and try again"}, 401
    # check user existense
    checker = db.cursor()
    checker.execute("SELECT username, email, password FROM users")
    for user in checker.fetchall():
        if user_email == user[1]:
            if check_password_hash(user[2], user_password):
                return {"status": "success", "Message": "Login successful"}, 200
            return {"status":"fail", "message":"Oops! check your details and try again"}, 401
