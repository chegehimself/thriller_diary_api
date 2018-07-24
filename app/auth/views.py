"""
app/auth/views.py
"""
import re
from flask import Blueprint, request, make_response, jsonify
from flask_api import FlaskAPI

# authentication blueprint

AUTH = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')


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

@AUTH.route('/register', methods = ['POST'])
def register():
    """ to register users """
    username = str(request.data.get('username', '')).strip()
    password = str(request.data.get('password', ''))
    email = str(request.data.get('email'), '')

    if username and password and email:
        return "ok data is fine", 200
    return "oops", 401