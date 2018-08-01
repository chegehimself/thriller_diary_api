import psycopg2
import os
HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE, port=5432)
cur = db.cursor()
cur.execute("""CREATE TABLE kim ( 
    ID serial PRIMARY KEY,
    username VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL,
    password VARCHAR (255));
    """)
cur.execute("""CREATE TABLE entries (
    ID serial PRIMARY KEY,
    title VARCHAR (255) NOT NULL,
    date_created VARCHAR (255) NOT NULL,
    description VARCHAR (255) NOT NULL,
    owner_id integer NOT NULL);
    """)
db.commit()