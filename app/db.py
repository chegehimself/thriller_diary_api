import psycopg2

class Connection(object):

    def __init__(self):

        self.HOSTNAME = 'ec2-107-22-169-45.compute-1.amazonaws.com'
        self.USERNAME = 'xqvzxugpqzozsl'
        self.PASSWORD = '6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494'
        self.DATABASE = 'dbmjf8qhfukq3i'
        self.db = psycopg2.connect( host=self.HOSTNAME, user=self.USERNAME, password=self.PASSWORD, dbname=self.DATABASE, port=5432)

    def db_return(self):
        return self.db