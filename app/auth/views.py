"""
app/auth/views.py
"""
import psycopg2
import re
from flask import Blueprint, request, jsonify
from flask_api import FlaskAPI
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flasgger import Swagger
from flasgger.utils import swag_from

# authentication blueprint

AUTH = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')

# from app.models import Accounts

from app.db import Connection

from app.models import User

user = User()

conn = Connection()

db = conn.db_return()

@AUTH.route('/', methods=['GET'])
@swag_from('/docs/index.yml')
def index():
    """ root """
    if request.method == 'GET':
        
        # the following is a welcoming message (at the landing page)
        welcome_message = {"Message": [{
            "Welcome":"Hey! welcome to thriller diary api"
            }]}

        response = {"status": "success", "Message": welcome_message}
        return response, 200

@AUTH.route('/signup', methods=['POST'])
@swag_from('/docs/signup.yml')
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
    
    user.register_user(username, user_email, user_password)
    response = {"status": "success", "Registered": {"Email":str(user_email), "Username":str(username)}}
    return response, 201

@AUTH.route('/login', methods=['POST'])
@swag_from('/docs/login.yml')
def login():
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
    elif user_email:
        user.login_user(user_email, user_password)
    else:
        return {"status":"fail", "message": "Oops! check your details and try again"}, 401
