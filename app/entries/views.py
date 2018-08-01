"""
app/views.py
contains routes
"""
from app.db import Connection
import re
import psycopg2

from flask import Blueprint, request

from app.models import token_required

from flasgger.utils import swag_from
# import models
from app.models import Entry, User
ENTRY = Entry()


CONN = Connection()

db = CONN.db_return()

user = User()

# create entries and a single entry Blueprint and
# version the urls to have '/api/v1' prefix
ENTRIES_BP = Blueprint('entries', __name__, url_prefix='/api/v1')

# deal with single entry
ENT_BP = Blueprint('ent', __name__, url_prefix='/api/v1')

@ENTRIES_BP.route('/entries', methods=['GET'])
@token_required
@swag_from('/docs/get_entries.yml')
def get_all_entries(current_user):
    """Retrives all Entries"""
    if request.method == 'GET':
        return ENTRY.all_entries(current_user)

@ENTRIES_BP.route('/entries', methods=['POST'])
@token_required
@swag_from('/docs/add_entry.yml')
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
    ENTRY.add_entry(title, description, current_user)
    response = {"status": "success", "entry": {"title":str(title), "description":str(description)}}
    return response, 201

@ENT_BP.route('/entries/<int:id_entry>', methods=['GET'])
@token_required
@swag_from('/docs/get_single.yml')
def fetch_single_entry(current_user, id_entry):
    """ will return a single entry """
    return ENTRY.return_single_entry(current_user, id_entry)

@ENT_BP.route('/entries/<int:id_entry>', methods=['PUT'])
@token_required
@swag_from('/docs/modify.yml')
def update_single_entry(current_user, id_entry):
    """ Edits a single entry """
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
    return ENTRY.edit_entry(current_user, id_entry, description, title)

@ENT_BP.route('entries/<int:id_entry>', methods=["DELETE"])
@token_required
@swag_from('/docs/delete.yml')
def delete_entry(current_user, id_entry):
    """ get rid of an entry """
    return ENTRY.delete_entry(current_user, id_entry)