"""
# tests/test_auth.py

# For unit testing of entries

# standard unittest
"""
import unittest
from app import create_app
from app.auth.views import db

class TestAuth(unittest.TestCase):
    """test for successful and unsuccessful entry auth"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {"username":"superman", "email":"superman@gmail.com", "password":"69mansuper"}
        self.register_route = 'api/v1/auth/signup'
        self.login_route = 'api/v1/auth/login'

    def test_registration_conflict(self):
        req = self.client().post(self.register_route, data=self.user) # pylint: disable=unused-variable
        req1 = self.client().post(self.register_route, data=self.user) # pylint: disable=unused-variable
        self.assertEqual(req1.status_code, 409)
    
    def test_registration_success(self):
        self.register = {"username":"spinderman7", "password":"spinderman7", "email":"spinderman7@gmail.com"}
        req = self.client().post(self.register_route, data=self.register) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 201)

    def test_login_success(self):
        self.user_data = {"email":"superman@gmail.com", "password":"69mansuper"}
        req = self.client().post(self.login_route, data=self.user_data) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 200)
    
    def test_invalid_input(self):
        self.user_data_empty = {"email":""}
        self.user_data_invalid_username = {"username":"#$superman", "email":"superman@gmail.com", "password":"69mansuper"}
        self.user_short_password = {"username":"superman", "email":"superman@gmail.com", "password":"i"}
        self.user_data_invalid_email = {"username":"superman", "email":"supermangmail.com", "password":"69mansuper"}
        req = self.client().post(self.register_route, data=self.user_data_empty)
        req1 = self.client().post(self.login_route, data=self.user_data_empty) # pylint: disable=unused-variable
        req2 = self.client().post(self.register_route, data=self.user_data_invalid_email)
        req3 = self.client().post(self.register_route, data=self.user_data_invalid_username)
        req4 = self.client().post(self.register_route, data=self.user_short_password)
        self.assertEqual(req4.status_code, 401)
        self.assertEqual(req1.status_code, 401)
        self.assertEqual(req2.status_code, 401)
        self.assertEqual(req3.status_code, 401)
        self.assertEqual(req.status_code, 401)
    
