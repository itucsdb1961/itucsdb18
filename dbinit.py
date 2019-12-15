import os
import sys

import psycopg2 as dbapi2

url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"

def init_book_table(url):
	statement = '''
		CREATE TABLE BOOKS(
			ID SERIAL,
			NAME VARCHAR(80) NOT NULL,
			PB_YR CHAR(4) NOT NULL,
			PB_LOC VARCHAR(80),
			PUBLISHER VARCHAR(80),
			GENRE VARCHAR(20),
			LANG VARCHAR(20),
			COUNT INT DEFAULT 1 NOT NULL,


			UNIQUE(NAME,PB_YR),
			PRIMARY KEY(ID)

		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()


def init_author_table(url):

	statement = '''
		CREATE TABLE AUTHORS(
			ID SERIAL,
			NAME VARCHAR(40) NOT NULL,
			LAST_NAME VARCHAR(40) NOT NULL,
			BIRTH_YR CHAR(4),
			BIRTH_PLACE VARCHAR(40),
			LAST_BOOK_DATE VARCHAR(40),
			LAST_BOOK_NAME VARCHAR(40),

			UNIQUE(NAME, LAST_NAME),
			PRIMARY KEY(ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()


def init_student_table(url):

	statement = '''
		CREATE TABLE STUDENTS(
			ID SERIAL,
			STUDENT_NUM CHAR(9) NOT NULL,
			NAME VARCHAR(40) NOT NULL,
			LAST_NAME VARCHAR(40) NOT NULL,
			FACULTY VARCHAR(40) NOT NULL,
			DEPART VARCHAR(40) NOT NULL,
			GRADE CHAR(1) NOT NULL,
			MEM_DATE VARCHAR(40) NOT NULL,
			DEBT FLOAT,

			UNIQUE(STUDENT_NUM),
			PRIMARY KEY(ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()

def init_relation_table_book_author(url):

	statement = '''
		CREATE TABLE BOOK_AUTHORS(
			BOOK_ID INT  REFERENCES BOOKS(ID),
			AUTHOR_ID INT REFERENCES AUTHORS(ID),

			UNIQUE (BOOK_ID,AUTHOR_ID),
			PRIMARY KEY(BOOK_ID,AUTHOR_ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()

def init_relation_table_student_lendbook(url):

	statement = '''
		CREATE TABLE STUDENT_BOOKS(
			BOOK_ID INT  REFERENCES BOOKS(ID),
			STUDENT_ID INT REFERENCES STUDENTS(ID),

			DATE_LEND FLOAT NOT NULL,

			UNIQUE (BOOK_ID,STUDENT_ID),
			PRIMARY KEY(BOOK_ID,STUDENT_ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()

def init_closets_table(url):

	statement = '''
		CREATE TABLE CLOSETS(
			ID SERIAL,
			CLOSET_FLOOR VARCHAR(40) NOT NULL,
			BLOCK VARCHAR(40) NOT NULL,
			CLOSET_NUMBER VARCHAR(40) NOT NULL,
			CLOSET_TYPE VARCHAR(40) NOT NULL,
			SIZE VARCHAR(40) NOT NULL,
			RETURN_HOUR CHAR(40) NOT NULL,

			UNIQUE(CLOSET_FLOOR,CLOSET_NUMBER),
			PRIMARY KEY(ID)
		)'''
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		connection.commit()

def init_user_table(url):

	statement = '''
		CREATE TABLE USERS(
			ID SERIAL,
			USERNAME VARCHAR(40) NOT NULL,
			H_PASSWORD VARCHAR(250) NOT NULL,
			ACCESS_LEVEL INT DEFAULT 3,

			UNIQUE(USERNAME),
			PRIMARY KEY(ID)
		)'''

	adm = "admin123"
	psw = "psw123"

	add_admin = '''
		INSERT INTO
		USERS (USERNAME, H_PASSWORD, ACCESS_LEVEL)
		VALUES 	('%s', '%s', %d)
		ON CONFLICT(BOOK_ID, STUDENT_ID) DO NOTHING
	''' % (adm , psw, 0)

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		cursor.execute(add_admin)

def init_shelf_table(url):

	statement = '''
		CREATE TABLE SHELVES(
			ID SERIAL,
			NUM INT NOT NULL,
			BLOCK INT NOT NULL,
			FLR INT NOT NULL,
			BOOK_TYPE VARCHAR(40),
			CAPACITY INT NOT NULL,

			UNIQUE(NUM,BLOCK,FLR),
			PRIMARY KEY(ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)

def init_relatin_table_shelf_book(url):

	statement = '''
		CREATE TABLE SHELF_BOOKS(
			BOOK_ID INT  REFERENCES BOOKS(ID),
			SHELF_ID INT REFERENCES SHELVES(ID),

			UNIQUE (BOOK_ID,SHELF_ID),
			PRIMARY KEY(BOOK_ID,SHELF_ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)

def wipe(url):

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS STUDENT_BOOKS")
		cursor.execute("DROP TABLE IF EXISTS BOOK_AUTHORS")
		cursor.execute("DROP TABLE IF EXISTS BOOKS")
		cursor.execute("DROP TABLE IF EXISTS AUTHORS")
		cursor.execute("DROP TABLE IF EXISTS STUDENTS")
		cursor.execute("DROP TABLE IF EXISTS CLOSETS")
		cursor.execute("DROP TABLE IF EXISTS USERS")
		cursor.execute("DROP TABLE IF EXISTS SHELVES")

def init_db(url):
	wipe(url)
	init_book_table(url)
	init_author_table(url)
	init_student_table(url)
	init_closets_table(url)
	init_shelf_table(url)
	init_user_table(url)
	init_relation_table_book_author(url)
	init_relation_table_student_lendbook(url)

#init_db(url)
