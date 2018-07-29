import psycopg2

class Connection(object):

    def __init__(self):
        # ########### OFFICIAL DB CREDENTIALS ##############
        # self.HOSTNAME = 'ec2-107-22-169-45.compute-1.amazonaws.com'
        # self.USERNAME = 'xqvzxugpqzozsl'
        # self.PASSWORD = '6e44c7de8ec9eb08db8f5b58080378cd1c3c6bc4f4beec842949d915c4488494'
        # self.DATABASE = 'dbmjf8qhfukq3i'

        ######## Credentials for tests ############
        # "dbname=d5pkbo1rnnpott 
        # host=ec2-50-16-241-91.compute-1.amazonaws.com 
        # port=5432 
        # user=tkvjvlrggrkghq
        # password=d65251fe55f72480c2bcec57179f094140167876bd903fc90b36da69f24e8d50

        """ connecting from the command line """
        # psql -U tkvjvlrggrkghq -h ec2-50-16-241-91.compute-1.amazonaws.com  -p 5432 -d d5pkbo1rnnpott
        
        # local connection
        # self.HOSTNAME = 'localhost'
        # self.USERNAME = 'postgres'
        # self.PASSWORD = '2grateful'
        # self.DATABASE = 'tests'

        # heroku testing db
        self.HOSTNAME = 'ec2-50-16-241-91.compute-1.amazonaws.com'
        self.USERNAME = 'tkvjvlrggrkghq'
        self.PASSWORD = 'd65251fe55f72480c2bcec57179f094140167876bd903fc90b36da69f24e8d50'
        self.DATABASE = 'd5pkbo1rnnpott'
        self.db = psycopg2.connect( host=self.HOSTNAME, user=self.USERNAME, password=self.PASSWORD, dbname=self.DATABASE, port=5432)

    def db_return(self):
        return self.db
