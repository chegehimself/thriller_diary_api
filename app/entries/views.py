"""
app/views.py
contains routes
"""
import re
import psycopg2

from flask import Blueprint, request
from app.models import token_required
from flasgger import Swagger
from flasgger.utils import swag_from
# import models
from app.models import Entry
ENTRY = Entry()

from app.db import Connection

conn = Connection()

db = conn.db_return()

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
        cur = db.cursor()
        cur.execute("SELECT * FROM entries")
        certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
        response = {"status": "success", "Entries": certain_user_entries}
        return response, 200

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
    cur = db.cursor()
    cur.execute("SELECT * FROM entries")
    certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
    entries_user = [an_entry for an_entry in certain_user_entries if an_entry[0] == id_entry]
    if len(entries_user) == 0:
      return {"status":"fail", "message":"you don't have such an entry"}, 404
    else:
        entry_id = entries_user[0][0]
        title = entries_user[0][1]
        date_created = entries_user[0][2]
        description = entries_user[0][3]
        response = {"status": "success", "entry": {"id":entry_id,
                                            "title":str(title),
                                            "description":str(description),
                                            "created":date_created}}
        return response, 200

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
    cur = db.cursor()
    cur.execute("SELECT * FROM entries")
    certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
    if len(certain_user_entries) == 0:
      return {"status":"fail", "message":"you don't have such an entry"}, 404
    if certain_user_entries[0][0] != id_entry:
        return {"status":"fail", "message":"that is not one of your entries fetch all to see your entries' ids"}, 404
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

@ENT_BP.route('entries/<int:id_entry>', methods=["DELETE"])
@token_required
@swag_from('/docs/delete.yml')
def delete_entry(current_user, id_entry):
    cur = db.cursor()
    cur.execute("SELECT * FROM entries")
    certain_user_entries = [entry for entry in cur.fetchall() if entry[4] == current_user]
    if len(certain_user_entries) == 0:
      return {"status":"fail", "message":"you don't have such an entry"}, 404
    if certain_user_entries[0][0] != id_entry:
        return {"status":"fail", "message":"tha is not one of your entries fetch all to see your entries' ids"}, 404
    query = "DELETE from entries WHERE entries.id = (%s)"
    cur.execute(query, [id_entry])
    db.commit()
    response = {
        "status":"success",
        "Deleted":{"id":id_entry}
    }
    return response, 200
