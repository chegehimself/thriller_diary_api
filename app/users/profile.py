from flask import request, Blueprint

from werkzeug.security import generate_password_hash, check_password_hash

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

@USERS_BP.route('/change_password', methods=["PUT"])
@token_required
def change_password(current_user):
    """
This route updates user's password
    Call this api route passing old_password, new_password and confirmation to update password at Thriller Diary Api (Token Required!)
    ---
    tags:
      - Routes
    parameters:
      - in: header
        name: access-token
        required: true
        type: string
      - in: body
        name: MewPassword
        description: The new password
        required: true
        schema:
          type: object
          required:
            -old_password
            -new_password
            -confirmation
          properties:
            old_password:
              type: string
              example: strongestpassword
            new_password:
              type: string
              example: jumanji
            confirmation:
              type: string
              example: jumanji
    responses:
      500:
        description: Error There was a server error!
      201:
        description: user password has been updated
      403:
        description: Method is not allowed
"""
    old_password = str(request.data.get('old_password', '')).strip()
    new_password = str(request.data.get('new_password', ''))
    confirmation = str(request.data.get('confirmation', ''))
    if not old_password or not new_password or not confirmation:
        return {"status":"fail","message":"please input all the fields"}, 401
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    certain_user = [user for user in cur.fetchall() if user[0] == current_user]
    if not check_password_hash(certain_user[0][3], old_password):
                return {"status":"fail", "message":"Incorrect old password"}, 401
    elif check_password_hash:
        new = new_password
        confirmnew = confirmation
        if new != confirmnew:
            return {"status":"fail", "message":"Password mismatch"}, 401
        else:
            new = new_password
            hashed_password = generate_password_hash(new, method='sha256')
            query = "UPDATE users SET password=(%s) WHERE id = (%s)"
            data = (hashed_password, current_user)
            cur.execute(query, data)
            db.commit()
            response = {
                "status": "success",
                "entry": {"Message":"Password Updated successfully"}}
            return response, 201

