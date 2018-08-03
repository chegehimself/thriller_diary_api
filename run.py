# run.py

# for running the server

# import app and blueprints

import os
from flask import redirect
from app import create_app
from flasgger import Swagger

# start the app in the set env mode
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

Swagger(app, template={
       "info": {
       "title": "Thriller diary API Version 1.0",
       "description": "API that will help users to pin down their thoughts and feelings. Find source code and guidelines on 'https://github.com/james-chege/thriller_diary_api'"},
       "securityDefinitions":{
           "TokenHeader": {
               "type": "apiKey",
               "name": "access-token",
               "in": "header"          
           }
       }
   })

@app.route("/")
def main():
    return redirect('/apidocs')

if __name__ == '__main__':
    app.run()
