"""
# tests/test_entries.py

# For unit testing of entries

# standard unittest
"""
import unittest
from app import create_app
# import Entry classe from models
from app.models import Entry

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

    def test_entry_adding_success(self):
        """returns True if entry addition was successful"""
        result = self.ent.add_entry("At Russia", "some good description of world cup experience")
        self.assertEqual(True, result)

    def test_entry_adding_failure(self):
        """returns False if an entry addition failed"""
        result = self.ent.add_entry("title", "")
        self.assertEqual(False, result)

    def test_get_all_entries(self):
        """ Test fetch all entries """
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry) # pylint: disable=unused-variable
        req_all = self.client().get(self.entry_route)
        self.assertEqual(req_all.status_code, 200)
        self.assertIn('At Russia', str(req_all.data))

    def test_entries_contains_nothing(self):
        """ Test fetch all entries """
        req_all = self.client().get(self.entry_route)
        self.assertEqual(req_all.status_code, 200)

    def test_entry_creation(self):
        """Test entry creation via post method"""
        # bind the app to the current context
        with self.app.app_context():
            req = self.client().post(self.entry_route, data=self.entry)
            req2 = self.client().post(self.entry_route, data=self.entry_bad_title)
            req3 = self.client().post(self.entry_route, data=self.entry_no_description)
            req4 = self.client().post(self.entry_route, data=self.entry_no_title)
            self.assertEqual(req2.status_code, 401)
            self.assertEqual(req3.status_code, 401)
            self.assertEqual(req4.status_code, 401)
            self.assertEqual(req.status_code, 201)
            self.assertIn('At Russia', str(req.data))

    def test_landing_page_message(self):
        """ Test Landing page message"""
        req = self.client().get('/api/v1/')
        self.assertEqual(req.status_code, 200)

    def test_fetch_single_entry(self):
        """ Test fetch single entry """
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry) # pylint: disable=unused-variable
        req_single = self.client().get(self.single_entry_route)
        self.assertEqual(req_single.status_code, 200)
        self.assertIn('At Russia', str(req_single.data))

    def test_modify_single_entry(self):
        """ Test editing of single entry """
         # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry) # pylint: disable=unused-variable
        req_single = self.client().put(self.single_entry_route, data=self.entry_new)
        req2 = self.client().put(self.single_entry_route, data=self.entry_bad_title)
        req3 = self.client().put(self.single_entry_route, data=self.entry_no_description)
        req4 = self.client().put(self.single_entry_route, data=self.entry_no_title)
        self.assertEqual(req2.status_code, 401)
        self.assertEqual(req3.status_code, 401)
        self.assertEqual(req4.status_code, 401)
        self.assertEqual(req_single.status_code, 201)
        self.assertIn('At Beach', str(req_single.data))

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
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.entry = {'title':'At Russia', 'description':'Me and my three friends decided ...'}
        self.single_entry_route = 'api/v1/entries/1'
        self.entry_route = 'api/v1/entries/'
        self.unavailable_id_route = 'api/v1/entries/300'

    def test_deletion_on_empty_entries(self):
        """ Test for deletion on empty"""
        req = self.client().delete(self.single_entry_route)
        self.assertNotEqual(req.status_code, 404)

    def test_deletion_success(self):
        """ test for successful entry deletion """
        # Not neccessary to use the following variable so pylint unused variable warning is disabled
        req = self.client().post(self.entry_route, data=self.entry) # pylint: disable=unused-variable
        delete_req = self.client().delete('api/v1/entries/2')
        self.assertEqual(delete_req.status_code, 200)

    # def test_delete_fail_on_unavailable_id(self):
    #     """ Test for deletion on unavailable entry """
    #     req = self.client().post(self.entry_route, data=self.entry)
    #     delete_req = self.client().delete(self.unavailable_id_route)
    #     self.assertEqual(delete_req.status_code, 404)

class TestProductionError(unittest.TestCase):
    """Test Server error in production environemnt """
    def setUp(self):
        self.app = create_app(config_name="production")
        self.client = self.app.test_client
    def test_error_500(self):
        """ Test for server error"""
        req = self.client().put('/api/v1/entries/1')
        self.assertEqual(req.status_code, 500)
