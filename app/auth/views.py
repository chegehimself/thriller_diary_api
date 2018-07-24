"""
app/auth/views.py
"""

from flask import Blueprint, request
from flask_api import FlaskAPI

# authentication blueprint

AUTH = Blueprint('authentication', __name__, url_prefix='/api/v1')


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