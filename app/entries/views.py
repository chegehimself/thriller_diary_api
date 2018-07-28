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

from app.db import Connection

conn = Connection()

db = conn.db_return()
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
    ENTRY.add_entry(title, description, current_user)
    response = {"status": "success", "entry": {"title":str(title), "description":str(description)}}
    return response, 201

@ENT_BP.route('/entries/<int:id_entry>', methods=['GET'])
@token_required
def fetch_single_entry(current_user, id_entry):
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
