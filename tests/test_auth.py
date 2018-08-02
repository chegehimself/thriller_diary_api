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
        """ test registration conflict """
        req = self.client().post(self.register_route, data=self.user) # pylint: disable=unused-variable
        req1 = self.client().post(self.register_route, data=self.user) # pylint: disable=unused-variable
        self.assertEqual(req1.status_code, 409)
        self.assertIn('exists', str(req1.data))
        
    
    def test_registration_success(self):
        """ test registration success """
        self.register = {"username":"spinderman", "password":"spinderman", "email":"spinderman@gmail.com"}
        req = self.client().post(self.register_route, data=self.register) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 201)
        self.assertIn('success', str(req.data))

    def test_login_success(self):
        """ test login success """
        self.user_data = {"email":"thor@gmail.com", "password":"thor"}
        req = self.client().post(self.login_route, data=self.user_data) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 200)
        self.assertIn('token', str(req.data))

    def test_login_while_not_registered(self):
        """ test not registered login """
        self.user_data = {"email":"fakethor@gmail.com", "password":"thor"}
        req = self.client().post(self.login_route, data=self.user_data) # pylint: disable=unused-variable
        self.assertEqual(req.status_code, 404)
        self.assertIn('check your details', str(req.data))
    
    def test_invalid_username(self):
        """ test for invalid username """
        self.user_data_invalid_username = {"username":"#$superman", "email":"superman@gmail.com", "password":"69mansuper"}
        req3 = self.client().post(self.register_route, data=self.user_data_invalid_username)
        self.assertEqual(req3.status_code, 401)
        self.assertIn('Invalid username', str(req3.data))

    def test_invalid_password(self):
        """ test for invalid password """
        self.user_short_password = {"username":"superman", "email":"superman@gmail.com", "password":"i"}
        self.user_wrong_password = {"username":"thor", "email":"thor@gmail.com", "password":"verywrong"}
        req4 = self.client().post(self.register_route, data=self.user_short_password)
        req5 = self.client().post(self.login_route, data=self.user_wrong_password)
        req7 = self.client().post(self.login_route, data=self.user_short_password)
        self.assertEqual(req4.status_code, 401)
        self.assertIn('short', str(req4.data))
        self.assertEqual(req5.status_code, 401)
        self.assertIn('Oops!', str(req5.data))
        self.assertEqual(req7.status_code, 401)
        self.assertIn('short password', str(req7.data))

    def test_empty_data(self):
        """ test for empty data submission """
        self.user_data_empty = {"email":""}
        req = self.client().post(self.register_route, data=self.user_data_empty)
        req1 = self.client().post(self.login_route, data=self.user_data_empty)
        self.assertEqual(req1.status_code, 401)
        self.assertIn('Check your details', str(req1.data))
        self.assertEqual(req.status_code, 401)
        self.assertIn('Check your details', str(req.data))
        
    def test_invalid_email_inputs(self):
        self.user_invalid_email = {"username":"superman", "email":"supermangmailcom", "password":"blackspear"}
        self.user_data_invalid_email = {"username":"superman", "email":"supermangmail.com", "password":"69mansuper"}
        req2 = self.client().post(self.register_route, data=self.user_data_invalid_email)
        req6 = self.client().post(self.login_route, data=self.user_data_invalid_email)
        self.assertEqual(req2.status_code, 401)
        self.assertIn('Invalid email', str(req2.data))
        self.assertEqual(req6.status_code, 401)
        self.assertIn('Invalid email', str(req6.data))