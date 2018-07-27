# thriller_diary_api

# status
[![Build Status](https://travis-ci.org/james-chege/thriller_diary_api.svg?branch=develop)](https://travis-ci.org/james-chege/thriller_diary_api)
[![Coverage Status](https://coveralls.io/repos/github/james-chege/thriller_diary_api/badge.svg?branch=develop)](https://coveralls.io/github/james-chege/thriller_diary_api?branch=develop)

[__Live version__](http://api-thriller-diary.herokuapp.com/api/v1/auth)

[Api Documentation](http://api-thriller-diary.herokuapp.com/apidocs/)


### Local Installation

Fork this repository to your github account and clone from there(_NB: clone from your github account - after forking_).This will help you to contribute to this project.

[Create a python Virtual environment and Activate it](https://virtualenv.pypa.io/en/stable/). A virtual environment is effective when working on multiple projects. Each project will have its own development enviroment.

__Install Dependencies__(_Note: This should be done in the created virtual environment_)
```py
 pip install -r requirements.txt
```
__Set environment variable__
```py
 export APP_SETTINGS="development"
```

# setup Database
* make sure you have [__postgresql__](https://www.postgresql.org/download/linux/ubuntu/) installed and running properly.

* open the terminal and type the following commands to create the database and the required tables

```
- psql -U postgres

- CREATE DATABASE thriller;

- \connect thriller

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
  ```


__Start Server__
```py
python run.py
```

[__Use postman app to send request to app.__](https://www.getpostman.com/)
### Endpoints

The following is a list of available endpoints in this application

|EndPoint               | Functionality|
| ------------------------------------ | ------------------------ |
|POST api/v1/auth/signup    |Register a user|
|POST api/v1/auth/login |Login a user|
|GET api/v1/entries |fetch all entries|
|GET api/v1/entries/<int:entryId> |fetch a single entry|
|POST api/v1/entries |Add an entry|
|PUT api/v1/entries/<int:entryId> |modify an entry|

# Testing
py.test --cov=app
