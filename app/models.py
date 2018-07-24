"""
app/models.py
contains models for the app
"""
import psycopg2
import datetime

class Entry(object):
    """Add new entry"""
    # constructor
    def __init__(self):
        # all entries placeholder
        self.entries = []

    def add_entry(self, title, description):
        """Adds new entries"""

        if description and title:
            now = datetime.datetime.now()
            date_created = now.strftime("%Y-%m-%d %H:%M")

            # entry id
            entry_id = 1
            for i in self.entries:
                entry_id += 1
                if i['id'] == entry_id:
                    entry_id += 1
            single_entry_holder = dict()
            single_entry_holder['id'] = entry_id
            single_entry_holder['title'] = title
            single_entry_holder['description'] = description
            single_entry_holder['created'] = str(date_created)
            self.entries.append(single_entry_holder)
            # return true
            return 1

        # on failure to add return false
        return 0


    def all_entries(self):
        """Return available entries"""

        return self.entries
        

# class Accounts(object):
#     """ Register and login users """

#     def __init__(self):
#         self.users = []

#     def register_user(self, email, password):
#         user_placeholder = {}
#         user_placeholder['email'] = email
#         user_placeholder['password'] = password
#         self.users.append(user_placeholder)

#     def all_users(self):
#         return self.users

#     def login(self, email, password):
#         for user in self.users:
#             if (user['email'] == email and user['password'] == password):
#                 return True
#             return False
