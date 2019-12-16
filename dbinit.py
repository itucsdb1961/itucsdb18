import os
import sys

import psycopg2 as dbapi2

LOCAL = False
_url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"


from book_view import book
from author_view import author
from student_view import student
from closet_view import closet
from shelf_view import shelf

import time
import datetime

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
			RETURN_HOUR VARCHAR(40) NOT NULL,

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
		ON CONFLICT(USERNAME) DO NOTHING
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
			BOOK_GENRE VARCHAR(40),
			CAPACITY INT NOT NULL,

			UNIQUE(NUM,BLOCK,FLR),
			PRIMARY KEY(ID)
		)'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)

def init_relation_table_shelf_book(url):

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
		cursor.execute("DROP TABLE IF EXISTS SHELF_BOOKS")
		cursor.execute("DROP TABLE IF EXISTS BOOK_AUTHORS")
		cursor.execute("DROP TABLE IF EXISTS BOOKS")
		cursor.execute("DROP TABLE IF EXISTS AUTHORS")
		cursor.execute("DROP TABLE IF EXISTS STUDENTS")
		cursor.execute("DROP TABLE IF EXISTS CLOSETS")
		cursor.execute("DROP TABLE IF EXISTS USERS")
		cursor.execute("DROP TABLE IF EXISTS SHELVES")

def add_mock_data(url):

	books = []

	tmp_book = book("Pride and Prejudice", "2000", "English", "Classics", "USA / CAN", "Modern Library")
	books.append(tmp_book)
	tmp_book = book("Animal Farm", "2003", "English", "Dystopia", "USA", "NA")
	books.append(tmp_book)
	tmp_book = book("The Picture of Dorian Gray", "2004", "English", "Classics", "USA", "Modern Library")
	books.append(tmp_book)
	tmp_book = book("Les Miserables", "1987", "English", "Classics", "USA", "Signet Classics")
	books.append(tmp_book)
	tmp_book = book("Romeo and Juliet", "2004", "English", "Classics", "USA", "Simon Schuster")
	books.append(tmp_book)

	for b in books:
		b.add_to_db(url)
	##################### 5 - BOOK ADDED

	authors = []

	tmp_author = author("Jane", "Austen")
	authors.append(tmp_author)
	tmp_author = author("George", "Orwell")
	authors.append(tmp_author)
	tmp_author = author("Oscar", "Wilde")
	authors.append(tmp_author)
	tmp_author = author("Victor", "Hugo")
	authors.append(tmp_author)
	tmp_author = author("William", "Shakespeare")
	authors.append(tmp_author)

	for a in authors:
		a.add_to_db(url)
	###################### 5 - AUTHOR ADDED



	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		for x in range(0,5):

			a_id = int(authors[x].fetch_id(url))
			b_id = int(books[x].fetch_id(url))

			cursor.execute('''
				INSERT INTO
				BOOK_AUTHORS (BOOK_ID, AUTHOR_ID)
				VALUES 	(%d, %d)
				ON CONFLICT(BOOK_ID, AUTHOR_ID) DO NOTHING
			''' % (b_id, a_id)
			)
	#################### BOOK_AUTHOR RELATIONS ADDED

	students = []

	tmp_student = student("150170004", "Salih Furkan" , "Ceyhan" , "Comp&Inf.Eng", "Comp Eng.", "2", time.time())
	students.append(tmp_student)

	for s in students:
		s.add_to_db(url)
	#################### STUDENT ADDED

	closets = []

	tmp_closet = closet("1","3","4","1","3", '''%s''' % (str(datetime.datetime.now())))
	closets.append(tmp_closet)

	tmp_closet = closet("1","4","7","2","2", '''%s''' % (str(datetime.datetime.now())))
	closets.append(tmp_closet)

	tmp_closet = closet("2","1","3","1","3", '''%s''' % (str(datetime.datetime.now())))
	closets.append(tmp_closet)

	tmp_closet = closet("0","3","4","1","3", '''%s''' % (str(datetime.datetime.now())))
	closets.append(tmp_closet)

	tmp_closet = closet("0","5","1","3","3", '''%s''' % (str(datetime.datetime.now())))
	closets.append(tmp_closet)

	for c in closets:
		c.add_to_db(url)

	###############


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
	init_relation_table_shelf_book(url)
	add_mock_data(url)


if __name__ == "__main__":

    url = os.getenv("DATABASE_URL", _url)

    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py")
        sys.exit(1)
    init_db(url)