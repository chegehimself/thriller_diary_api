"""
app/auth/views.py
"""
import re
from flask import Blueprint, request, make_response, jsonify
from flask_api import FlaskAPI

# authentication blueprint

AUTH = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')

from app.models import Accounts
ACCOUNT = Accounts()

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

@AUTH.route('/signup', methods=['POST'])
def user_registration():
    email = str(request.data.get('email', '')).strip()
    password = str(request.data.get('password', ''))
    ACCOUNT.register_user(email, password)
    response = {"status": "success", "Registered": {"Email":str(email), "Password":str(password)}}
    return response, 201

# @AUTH.route('/users', methods=['GET'])
# def all_users():
#     response = {"status": "success", "users": ACCOUNT.all_users()}
#     return response, 200

@AUTH.route('/login', methods=['POST'])
def login():
    email = str(request.data.get('email', '')).strip()
    password = str(request.data.get('password', ''))
    if not ACCOUNT.all_users():
        return  {"status": "Fail", "message": "Such a user doesnot exist"}
    for user in ACCOUNT.all_users():
        if user['email'] == email and user['password'] == password:
            response =  {"status": "success", "message": "Login successful"}
            return response, 200
        response =  {"status": "Fail", "message": "Check credentials and try again"}
        return response, 401
        