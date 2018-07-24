"""
app/auth/views.py
"""
import psycopg2
import re
from flask import Blueprint, request, make_response, jsonify
from flask_api import FlaskAPI

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
    cur.execute("SELECT username, email FROM users")
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
    # check user existense
    checker = db.cursor()
    checker.execute("SELECT username, email FROM users")
    for user in checker.fetchall():
        if username == user[0]:
            return {"status": "fail", "message" : "user exists"}, 409

    cur = db.cursor()
    query =  "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
    data = (user_email, user_password, username)
    cur.execute(query, data)
    db.commit()
    # ACCOUNT.register_user(email, password)
    response = {"status": "success", "Registered": {"Email":str(user_email), "Username":str(username), "Password":str(user_password)}}
    return response, 201

# @AUTH.route('/users', methods=['GET'])
# def all_users():
#     response = {"status": "success", "users": ACCOUNT.all_users()}
#     return response, 200

# @AUTH.route('/login', methods=['POST'])
# def login():
#     email = str(request.data.get('email', '')).strip()
#     password = str(request.data.get('password', ''))
#     if not ACCOUNT.all_users():
#         return  {"status": "Fail", "message": "Such a user doesnot exist"}
#     for user in ACCOUNT.all_users():
#         if user['email'] == email and user['password'] == password:
#             response =  {"status": "success", "message": "Login successful"}
#             return response, 200
#         response =  {"status": "Fail", "message": "Check credentials and try again"}
#         return response, 401
        