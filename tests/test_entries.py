"""
# tests/test_entries.py

# For unit testing of entries

# standard unittest
"""
import unittest
from app import create_app
# import Entry classe from models
from app.models import Entry
import json

from app.db import Connection

conn = Connection()

db = conn.db_return()

class TestDiaryEntry(unittest.TestCase):
    """test for successful and unsuccessful entry addition"""
    def setUp(self):
        self.ent = Entry()
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.entry = {'title':'At Russia', 'description':'Me and my three friends decided ...'}
        self.entry_new = {'title':'At Beach', 'description':'Me and my three friends decided ...'}
        self.entry_bad_title = {'title':'$', 'description':'Me and my three friends decided ...'}
        self.entry_no_title = {'title':'', 'description':'Me and my three friends decided ...'}
        self.entry_no_description = {'title':'At Beach', 'description':''}
        self.entry_route = 'api/v1/entries/'
        self.single_entry_route = 'api/v1/entries/1'
        self.unavailable_id_route = 'api/v1/entries/300'
        self.bad_url = '/api/v1/entries/not_available'

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

    def test_get_all_entries(self):
        """ Test fetch all entries """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        # obtain the access token
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token}) # pylint: disable=unused-variable
        req_all = self.client().get(self.entry_route, headers={"access-token":access_token})
        self.assertEqual(req_all.status_code, 200)
        self.assertIn('At Russia', str(req_all.data))
    def test_get_unavailable_entry(self):
        """ test for request of unavailable entry """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req = self.client().get('api/v1/entries/5', headers={"access-token":access_token})
        self.assertEqual(req.status_code, 404)
        self.assertIn('fail', str(req.data))
    
    def test_put_when_entries_empty(self):
        """ test for request of unavailable entry """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req = self.client().put('api/v1/entries/5', data=self.entry_new, headers={"access-token":access_token})
        self.assertEqual(req.status_code, 404)
        self.assertIn('fail', str(req.data))

    def test_delete_when_entries_empty(self):
        """ test for request of unavailable entry """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req = self.client().delete('api/v1/entries/5', headers={"access-token":access_token})
        self.assertEqual(req.status_code, 404)
        self.assertIn('fail', str(req.data))

    def test_entries_contains_nothing(self):
        """ Test fetch all entries """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req_all = self.client().get(self.entry_route, headers={"access-token":access_token})
        self.assertEqual(req_all.status_code, 200)

    def test_entry_creation(self):
        """Test entry creation via post method"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        # bind the app to the current context
        with self.app.app_context():
            req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token})
            req2 = self.client().post(self.entry_route, data=self.entry_bad_title, headers={"access-token":access_token})
            req3 = self.client().post(self.entry_route, data=self.entry_no_description, headers={"access-token":access_token})
            req4 = self.client().post(self.entry_route, data=self.entry_no_title, headers={"access-token":access_token})
            self.assertEqual(req2.status_code, 401)
            self.assertEqual(req3.status_code, 401)
            self.assertEqual(req4.status_code, 401)
            self.assertEqual(req.status_code, 201)
            self.assertIn('At Russia', str(req.data))
    def test_for_unavailable_id_fetch(self):
        """ test for fetch of an unavailable id """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token})  # pylint: disable=unused-variable
        req2 = self.client().get('api/v1/entries/10', headers={"access-token":access_token})
        self.assertEqual(req2.status_code, 404)
        self.assertIn('fail', str(req2.data))

    def test_for_unavailable_id_modification(self):
        """ test for modification of an unavailable id """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token})  # pylint: disable=unused-variable
        req2 = self.client().put('api/v1/entries/50', data=self.entry_new, headers={"access-token":access_token})
        self.assertEqual(req2.status_code, 404)
        self.assertIn('fail', str(req2.data))

    def test_for_delete_id_modification(self):
        """ test for modification of an unavailable id """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token})  # pylint: disable=unused-variable
        req2 = self.client().delete('api/v1/entries/50', data=self.entry_new, headers={"access-token":access_token})
        self.assertEqual(req2.status_code, 404)

    def test_landing_page_message(self):
        """ Test Landing page message"""
        req = self.client().get('/api/v1/auth')
        self.assertEqual(req.status_code, 200)
    def test_no_access_toke_provide(self):
        """ Test token no token provided"""
        req = self.client().get('/api/v1/entries')
        self.assertEqual(req.status_code, 401)
    def test_invalid_token(self):
        """ test invalid token"""
        req = self.client().get('/api/v1/entries', headers={"access-token":"invalid_access_token"})
        self.assertEqual(req.status_code, 401)
    def test_empty_token(self):
        """ test empty token"""
        req = self.client().get('/api/v1/entries', headers={"access-token":None})
        self.assertEqual(req.status_code, 401)

    def test_fetch_single_entry(self):
        """ Test fetch single entry """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token}) # pylint: disable=unused-variable
        req_single = self.client().get('api/v1/entries/1', headers={"access-token":access_token})
        self.assertEqual(req_single.status_code, 200)
        self.assertIn('At Russia', str(req_single.data))

    def test_modify_single_entry(self):
        """ Test editing of single entry """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
         # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":access_token}) # pylint: disable=unused-variable
        req_single = self.client().put(self.single_entry_route, data=self.entry_new, headers={"access-token":access_token})
        req2 = self.client().put(self.single_entry_route, data=self.entry_bad_title, headers={"access-token":access_token})
        req3 = self.client().put(self.single_entry_route, data=self.entry_no_description, headers={"access-token":access_token})
        req4 = self.client().put(self.single_entry_route, data=self.entry_no_title, headers={"access-token":access_token})
        # an entry that does not belong to the user
        req5 = self.client().put('api/v1/entries/2', data=self.entry_new, headers={"access-token":access_token})
        self.assertEqual(req5.status_code, 404)
        self.assertIn('not one of your entries', str(req5.data))
        self.assertEqual(req2.status_code, 401)
        self.assertEqual(req3.status_code, 401)
        self.assertEqual(req4.status_code, 401)
        self.assertEqual(req_single.status_code, 201)
        self.assertIn('success', str(req_single.data))

    def test_not_found_url(self):
        """ Test for unavailable url request """
        req = self.client().get(self.bad_url)
        self.assertEqual(req.status_code, 404)

    def test_error_405(self):
        """ Test for Method Not allowed """
        req = self.client().post(self.single_entry_route)
        self.assertEqual(req.status_code, 405)

class TestDeletion(unittest.TestCase):
    """ To test deletions """
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

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.entry = {'title':'At Russia', 'description':'Me and my three friends decided ...'}
        self.single_entry_route = 'api/v1/entries/84'
        self.entry_route = 'api/v1/entries/'
        self.unavailable_id_route = 'api/v1/entries/300'
        self.register_user()
        self.result = self.login_user()
        self.access_token = json.loads(self.result.data.decode())['token']

    def test_deletion_on_empty_entries(self):
        """ Test for deletion on empty"""
        req = self.client().delete(self.single_entry_route, headers={"access-token":self.access_token})
        self.assertEqual(req.status_code, 404)

    def test_deletion_success(self):
        """ test for successful entry deletion """
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":self.access_token}) # pylint: disable=unused-variable
        delete_req = self.client().delete('api/v1/entries/1', headers={"access-token":self.access_token})
        self.assertEqual(delete_req.status_code, 200)

    def test_delete_fail_on_unavailable_id(self):
        """ Test for deletion on unavailable entry """
        req = self.client().post(self.entry_route, data=self.entry, headers={"access-token":self.access_token}) # pylint: disable=unused-variable
        delete_req = self.client().delete(self.unavailable_id_route, headers={"access-token":self.access_token})
        self.assertEqual(delete_req.status_code, 404)

