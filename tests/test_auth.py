"""
# tests/test_auth.py

# For unit testing of entries

# standard unittest
"""
import unittest
from app import create_app

class TestDiaryEntry(unittest.TestCase):
    """test for successful and unsuccessful entry addition"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {"username":"superman", "email":"superman@gmail.com", "passowrd":"69mansuper"}
        self.register_route = 'api/v1/auth/signup'

    def test_registration(self):
        req = self.client().post(self.register_route, data=self.user) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 201)