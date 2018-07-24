"""
# tests/test_auth.py

# For unit testing of entries

# standard unittest
"""
import unittest
from app import create_app

class TestAuth(unittest.TestCase):
    """test for successful and unsuccessful entry addition"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {"username":"superman", "email":"superman@gmail.com", "passowrd":"69mansuper"}
        self.register_route = 'api/v1/auth/signup'
        self.login_route = 'api/v1/auth/login'

    def test_registration_success(self):
        req = self.client().post(self.register_route, data=self.user) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 201)

    def test_login_success(self):
        self.user_data = {"email":"superman@gmail.com", "passowrd":"69mansuper"}
        req = self.client().post(self.login_route, data=self.user_data) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 200)
