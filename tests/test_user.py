"""
# tests/test_users.py

# For unit testing of users

# standard unittest
"""
import unittest
from app import create_app
import json

from app.db import Connection

conn = Connection()

db = conn.db_return()

class TestDiaryEntry(unittest.TestCase):
    """test for successful and unsuccessful entry addition"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.users_route = '/api/v1/users/profile'
        self.correct_credentials = {'old_password':'thor', 'new_passowrd':'jumanji', "confirmation":"jumanji" }

        with self.app.app_context():
            cur = db.cursor()
            cur.execute('DELETE FROM "users";')
            cur.execute('DELETE FROM "entries";')
            db.commit()

    # login user
    def register_user(self, username="thor", email="thor@gmail.com", password="thor"):
        """register user."""
        user_data = {
            'username':username,
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/signup', data=user_data)

    def login_user(self, email="thor@gmail.com", password="thor"):
        """login user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/login', data=user_data)

    def test_get_user_info(self):
        """ Test fetch user  """
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['token']
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req_info = self.client().get(self.users_route, headers={"access-token":access_token})
        self.assertEqual(req_info.status_code, 200)
        self.assertIn('success', str(req_info.data))
        