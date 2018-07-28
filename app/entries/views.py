"""
app/views.py
contains routes
"""
import re
import psycopg2

from flask import Blueprint, request
from app.models import token_required
from flasgger import Swagger
# import models
from app.models import Entry
ENTRY = Entry()

# HOSTNAME = 'localhost'
# USERNAME = 'postgres'
# PASSWORD = '2grateful'
# DATABASE = 'thriller'
HOSTNAME = 'ec2-107-22-169-45.compute-1.amazonaws.com'
USERNAME = 'xqvzxugpqzozsl'
PASSWORD = '6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494'
DATABASE = 'dbmjf8qhfukq3i'
# db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE, port=5432)
db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE, port=5432 )

# call all available entries
ENTRIES = ENTRY.all_entries()

# create entries and a single entry Blueprint and
# version the urls to have '/api/v1' prefix
ENTRIES_BP = Blueprint('entries', __name__, url_prefix='/api/v1')

# deal with single entry
ENT_BP = Blueprint('ent', __name__, url_prefix='/api/v1')

# @ENTRIES_BP.route('/', methods=['GET'])
# def index():
#     if request.method == 'GET':

#         # the following is a welcoming message (at the landing page)
#         welcome_message = {"Message": [{
#             "Welcome":"Hey! welcome to thriller diary api"
#             }]}

#         response = {"status": "success", "Message": welcome_message}
#         return response, 200

@ENTRIES_BP.route('/entries', methods=['GET'])
@token_required
def get_all_entries(current_user):
    """
This is the route to get all diary entries
    Call this api route to see all user's diary entries Thriller Diary Api (Token Required!)
    ---
    tags:
      - Routes
    parameters:
      - in: header
        name: access-token
        required: true
        type: string
    responses:
      500:
        description: Error There was a server error!
      200:
        description: Entries has been displayed
      401:
        description: Token not provided or is invalid
      403:
        description: Method is not allowed
"""
    """Retrives all Entries"""
    if request.method == 'GET':
        cur = db.cursor()
        cur.execute("SELECT * FROM entries")
        certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
        response = {"status": "success", "Entries": certain_user_entries}
        return response, 200

@ENTRIES_BP.route('/entries', methods=['POST'])
@token_required
def add_new_entry(current_user):
    """
This is the route adds a new entry
    Call this api route passing a title and description to add an entry at Thriller Diary Api (Token Required!)
    ---
    tags:
      - Routes
    parameters:
      - in: header
        name: access-token
        required: true
        type: string
      - in: body
        name: entry
        description: The entry
        required: true
        schema:
          type: object
          required:
            -description
            -title
          properties:
            title:
              type: string
              example: At Beach
            description:
              type: string
              example: Me and my three friends decide to spend our saturday...
    responses:
      500:
        description: Error There was a server error!
      201:
        description: Entry has been created successfully
      401:
        description: wrong parameters were provided
      403:
        description: Method is not allowed
"""

    """Add an entry"""
    # json_data = request.get_json()
    title = str(request.data.get('title', '')).strip()
    description = str(request.data.get('description', ''))
    # check empty title
    if not title:
        response = {"message": "Please input title", "status": 401}
        return response, 401
    # check empty description
    if not description:
        response = {"message": "Please input description", "status": 401}
        return response, 401
    # check for special characters in title
    if not re.match(r"^[a-zA-Z0-9_ -]*$", title):
        response = {"message": "Please input valid title", "status": 401}
        return response, 401
    # title = json_data['title']
    # description = json_data['description']
    ENTRY.add_entry(title, description, current_user   )
    response = {"status": "success", "entry": {"title":str(title), "description":str(description)}}
    return response, 201

@ENT_BP.route('/entries/<int:id_entry>', methods=['GET'])
@token_required
def fetch_single_entry(current_user, id_entry):
    """
This is the route modifies fetches specified entry
    Call this api route passing a title and description to  an entry at Thriller Diary Api (Token Required!)
    ---
    tags:
      - Routes
    parameters:
      - in: header
        name: access-token
        required: true
        type: string
      - in: path
        name: id_entry
        description: id of entry to modify
        required: true
        type: number    
    responses:
      500:
        description: Error There was a server error!
      201:
        description: Entry has been updated successfully
      401:
        description: wrong parameters were provided
      403:
        description: Method is not allowed
"""

    """ will return a single entry """
    # if there are no entries there is no need to do anything
    # if not ENTRIES:
    #     return {"status": "Fail", "entry": {"Error":"That entry does not exist!"}}, 404
    cur = db.cursor()
    cur.execute("SELECT * FROM entries")
    certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
    for entry in certain_user_entries:
        # check if the entry exists and return
        if entry[0] == id_entry:
            title = entry[1]
            description = entry[3]
            date_created = entry[2]
            entry_id = entry[0]
            response = {
                "status": "success", "entry": {"id":entry_id,
                                               "title":str(title),
                                               "description":str(description),
                                               "created":date_created
                                              }}
            return response, 200

@ENT_BP.route('/entries/<int:id_entry>', methods=['PUT'])
@token_required
def update_single_entry(current_user, id_entry):
    """
This is the route modifies an new entry
    Call this api route passing an id to fetch a single entry at Thriller Diary Api (Token Required!)
    ---
    tags:
      - Routes
    parameters:
      - in: header
        name: access-token
        required: true
        type: string
      - in: path
        name: id_entry
        description: id of entry to fetch
        required: true
        type: number    
    responses:
      500:
        description: Error There was a server error!
      200:
        description: Entry has been found and displayed
      403:
        description: Method is not allowed
"""

    """ Edits a single entry """
    # if there are no entries there is no need to do anything
    # if not ENTRIES:
    #     return {"status": "Fail", "entry": {"Error":"That entry does not exist!"}}, 404
    # for entry in ENTRIES:
    #     # check if the entry exists
    #     if entry['id'] == id_entry:
    title = str(request.data.get('title', '')).strip()
    description = str(request.data.get('description', ''))
    # check for empty title
    if not title:
        response = {"message": "Please input title", "status": 401}
        return response, 401
    # check for empty description
    if not description:
        response = {"message": "Please input description", "status": 401}
        return response, 401
    # check for special characters in title
    if not re.match(r"^[a-zA-Z0-9_ -]*$", title):
        response = {"message": "Please input valid title", "status": 401}
        return response, 401   
    cur = db.cursor()
    cur.execute("SELECT * FROM entries")
    certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
    for entry in certain_user_entries:
        # update the entry
        query = "UPDATE entries SET description=(%s), title=(%s) WHERE id = (%s)"
        data = (description, title, id_entry)
        cur.execute(query, data)
        db.commit()
        response = {
            "status": "success",
            "entry": {"Message":"Updated successfully"}}
        return response, 201
