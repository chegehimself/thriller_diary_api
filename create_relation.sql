CREATE TABLE entries (
  ID serial PRIMARY KEY,
  title VARCHAR (255) NOT NULL,
  date_created VARCHAR (255) NOT NULL,
  description VARCHAR (255) NOT NULL,
  owner_id integer NOT NULL
  );