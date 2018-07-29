"""app/__init__.py - This file creates and initializes the app"""

import os
from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
# local import
from instance.config import APP_CONFIG
from app.models import Entry
from . entries.views import ENTRIES_BP, ENT_BP
from . auth.views import AUTH
from . users.profile import USERS_BP

def create_app(config_name):
    """ creates the app with the desired environment """
    # instantiate flask app
    app = FlaskAPI(__name__, instance_relative_config=True)
    
    # app settings config
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')

    # secret key
    app.config['SECRET_KEY'] = '@dinoIs@PandasNot@Shark'
    # for cross origin resource sharing
    CORS(app)
    # fix not found error(testing)
    app.url_map.strict_slashes = False
    # register the blueprints
    app.register_blueprint(ENTRIES_BP)
    app.register_blueprint(ENT_BP)
    app.register_blueprint(AUTH)
    app.register_blueprint(USERS_BP)

    # @app.route('/documentation', methos=['GET'])
    # def docs():
    #     return 

    # For the following functions pylint has been disabled only on variables and arguements
    # It is Not necessary to use the variables or the argument
    @app.errorhandler(404)
    def error_404(error=None):  # pylint: disable=unused-variable
        # pylint: disable=unused-argument
        """ handle request for unavailable url """
        message = {
            'status': '404',
            'message': request.url + ' Was not found in this server',
        }
        response = jsonify(message)
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def server_error(error=None):  # pylint: disable=unused-argument
        # pylint: disable=unused-variable
        """ handle server error """
        response = {"status": 500, "Message":"Something went wrong!"}
        return response, 500

    @app.errorhandler(405)
    def method_not_allowed(error=None): # pylint: disable=unused-variable
        # pylint: disable=unused-argument
        """ handle method not allowed """
        response = {"status": 405, "Message":"Method not allowed"}
        return response, 405
    return app
