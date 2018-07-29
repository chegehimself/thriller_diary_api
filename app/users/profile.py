from flask import request, Blueprint

from app.models import token_required

from app.db import Connection

conn = Connection()

db = conn.db_return()

# regester user blueprint

USERS_BP = Blueprint('users', __name__, url_prefix='/api/v1/users')

@USERS_BP.route('/profile', methods=["GET"])
@token_required
def profile(current_user):
    """
This route retrieves the user info
    Call this api route to see user's profile at Thriller Diary Api (Token Required!)
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
        description: User has been displayed
      401:
        description: Token not provided or is invalid
      403:
        description: Method is not allowed
"""
    """ retrive user details """
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    certain_user_entries = [entry for entry in cur.fetchall() if entry[0] == current_user]
    response = {"status": "success", "Profile": {"id":certain_user_entries[0][0],"username":certain_user_entries[0][1], "email":certain_user_entries[0][2]}}
    return response, 200
