"""
app/views.py
contains routes
"""
import re

from flask import Blueprint, request
# import models
from app.models import Entry
ENTRY = Entry()

# call all available entries
ENTRIES = ENTRY.all_entries()

# create entries and a single entry Blueprint and
# version the urls to have '/api/v1' prefix
ENTRIES_BP = Blueprint('entries', __name__, url_prefix='/api/v1')

# deal with single entry
ENT_BP = Blueprint('ent', __name__, url_prefix='/api/v1')

@ENTRIES_BP.route('/', methods=['GET'])
def index():
    """ root """
    if request.method == 'GET':

        # the following is a welcoming message (at the landing page)
        welcome_message = {"Message": [{
            "Welcome":"Hey! welcome to thriller diary api"
            }]}

        response = {"status": "success", "Message": welcome_message}
        return response, 200

@ENTRIES_BP.route('/entries', methods=['GET'])
def get_all_entries():
    """Retrives all Entries"""
    if request.method == 'GET':
        # if there is nothing yet
        if not ENTRIES:
            response = {"status": "success", "entries": "There are no entries for now"}
            return response, 200
        response = {"status": "success", "entries": ENTRIES}
        return response, 200

@ENTRIES_BP.route('/entries', methods=['POST'])
def add_new_entry():
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
    ENTRY.add_entry(title, description)
    response = {"status": "success", "entry": {"title":str(title), "description":str(description)}}
    return response, 201

@ENT_BP.route('/entries/<int:id_entry>', methods=['GET'])
def fetch_single_entry(id_entry):
    """ will return a single entry """
    # if there are no entries there is no need to do anything
    if not ENTRIES:
        return {"status": "Fail", "entry": {"Error":"That entry does not exist!"}}, 404
    for entry in ENTRIES:
        # check if the entry exists and return
        if entry['id'] == id_entry:
            title = entry['title']
            description = entry['description']
            date_created = entry['created']
            entry_id = entry['id']
            response = {
                "status": "success", "entry": {"id":entry_id,
                                               "title":str(title),
                                               "description":str(description),
                                               "created":date_created
                                              }}
            return response, 200

@ENT_BP.route('/entries/<int:id_entry>', methods=['PUT'])
def update_single_entry(id_entry):
    """ Edits a single entry """
    # if there are no entries there is no need to do anything
    if not ENTRIES:
        return {"status": "Fail", "entry": {"Error":"That entry does not exist!"}}, 404
    for entry in ENTRIES:
        # check if the entry exists
        if entry['id'] == id_entry:
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
            entry['title'] = title
            entry['description'] = description
            date_created = entry['created']

            response = {
                "status": "success",
                "entry": {"title":str(title),
                          "description":str(description),
                          "created":date_created}}
            return response, 201

@ENT_BP.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """ To delete a certain entry """
    # if there are no entries there is no need to do anything
    if not ENTRIES:
        return {"status": "Fail", "entry": {"Error":"That entry does not exist!"}}, 404
    for i, entry in  enumerate(ENTRIES):
        # check if the entry exists
        if entry['id'] == int(entry_id):
            title = entry['title']
            description = entry['description']
            date_created = entry['created']
            ENTRIES.pop(i)
            response = {"status": "success",
                        "Deleted": {"title":str(title),
                                    "description":str(description),
                                    "created":date_created}}
            return response, 200
