import psycopg2
HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '2grateful'
DATABASE = 'tests'
db = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE, port=5432)
cur = db.cursor()
cur.execute("""CREATE TABLE users ( 
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