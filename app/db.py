import psycopg2
import os
class Connection(object):
    """ creates connection to the database """

    def __init__(self):
        # ########### OFFICIAL DB CREDENTIALS ##############
        self.HOSTNAME = 'localhost'
        self.USERNAME = 'postgres'
        self.PASSWORD = os.getenv('PASSWORD')
        self.DATABASE = os.getenv('DATABASE')
        self.db = psycopg2.connect( host=self.HOSTNAME, user=self.USERNAME, password=self.PASSWORD, dbname=self.DATABASE, port=5432)

    def db_return(self):
        return self.db
