"""
app/models.py
contains models for the app
"""
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
        