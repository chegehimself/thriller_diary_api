# run.py

# for running the server

# import app and blueprints

import os
from app import create_app

# start the app in the set env mode
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
