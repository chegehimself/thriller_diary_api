# run.py

# for running the server

# import app and blueprints

import os
from app import create_app
from flasgger import Swagger

# start the app in the set env mode
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
Swagger(app)

if __name__ == '__main__':
    app.run()
