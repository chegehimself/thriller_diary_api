 CREATE TABLE users (
  ID serial PRIMARY KEY,
  username VARCHAR (255) NOT NULL,
  email VARCHAR (255) NOT NULL,
  password VARCHAR (255)
  );

CREATE TABLE entries (
  ID serial PRIMARY KEY,
  title VARCHAR (255) NOT NULL,
  date_created VARCHAR (255) NOT NULL,
  description VARCHAR (255) NOT NULL,
  owner_id integer NOT NULL,
  CONSTRAINT users_id_fkey FOREIGN KEY (id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  );