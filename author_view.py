url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template

class author:
	def __init__(self,
				name,
				last_name,
				birth_year = None,
				birth_place = None,
				last_book_date = None,
				last_book_name = None,
				):
		self.name = name
		self.last_name = last_name
		self.birth_year = birth_year
		self.birth_place = birth_place
		self.last_book_date = last_book_date
		self.last_book_name = last_book_name

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					AUTHORS	(NAME, LAST_NAME, BIRTH_YR, BIRTH_PLACE, LAST_BOOK_DATE, LAST_BOOK_NAME)
					VALUES 	('%s', '%s', '%s', '%s', '%s', '%s')
					ON CONFLICT(NAME, LAST_NAME) DO NOTHING
					''' % (self.name, self.last_name, self.birth_year, self.birth_place, self.last_book_date, self.last_book_name)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			connection.commit()

	def fetch_id(self,db_url):

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(
					'''
					select * from authors
					where
					NAME = '%s' and
					LAST_NAME = '%s'
					''' % (self.name, self.last_name)
					)
			ids = cursor.fetchall()
			return ids[0][0]


def admin_authors_page():

	authors = []
	statement = '''
		SELECT * FROM AUTHORS
	'''	

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "create":
				tmp_author = author(request.form["author_name"], request.form["last_name"] ,request.form["birth_year"], request.form["birth_place"], request.form["last_book_date"], request.form["last_book_name"])
				tmp_author.add_to_db(url)
			elif request.form["form_name"] == "filter":
				condition = []

				if request.form["author_name"]:
					condition.append("(NAME ~* '.*" + str(request.form["author_name"]) + ".*')")

				if request.form["author_surname"]:
					condition.append("(LAST_NAME ~* '.*" + str(request.form["author_surname"]) + ".*')")

				if len(condition):
					statement += " WHERE "
					
					first = True
					for cond in condition:
						if not first:
							statement += " AND "
						statement += cond				

	authors = []
	print("statement = " + statement)
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		authors = cursor.fetchall()
	return render_template("admin_authors.html", authors = authors)

def author_page(author_id):

	author = []
	books = []

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "update":

				updates = []

				if request.form["birth_year"]:
					updates.append("BIRTH_YR = " + str(request.form["birth_year"]))

				if request.form["birth_place"]:
					updates.append("BIRTH_PLACE = '" + str(request.form["birth_place"]) + "'")

				if request.form["last_book_date"]:
					updates.append("LAST_BOOK_DATE = '" + str(request.form["last_book_date"]) + "'")

				if request.form["last_book_name"]:
					updates.append("LAST_BOOK_NAME = '" + str(request.form["last_book_name"]) + "'")

				statement = "UPDATE AUTHORS SET "

				update_statement = ""
				first = True
				for update in updates:
					if not first:
						update_statement += " , "
					update_statement += update

				statement += update_statement

				where_statement = '''
					WHERE ID = %d
				''' % (int(author_id))

				statement += where_statement

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)



	statement_author = '''
		SELECT * FROM AUTHORS
		WHERE (ID = %d)
	''' % (int(author_id))

	statement_books = '''
		SELECT * FROM BOOK_AUTHORS
		WHERE (AUTHOR_ID = %d)
	''' % (int(author_id))

	with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute(statement_author)
			author = cursor.fetchall()

			cursor.execute(statement_books)
			books = cursor.fetchall()


	return render_template("author.html", author = author, books = books)

def authors_page():

	authors = []
	statement = '''
		SELECT * FROM AUTHORS
	'''

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from authors")
		authors = cursor.fetchall()

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "filter":
				condition = []

				if request.form["author_name"]:
					condition.append("(NAME ~* '.*" + str(request.form["author_name"]) + ".*')")

				if request.form["author_surname"]:
					condition.append("(LAST_NAME ~* '.*" + str(request.form["author_surname"]) + ".*')")

				if len(condition):
					statement += " WHERE "
					
					first = True
					for cond in condition:
						if not first:
							statement += " AND "
						statement += cond

				# final statement

	print("statement = " + statement)
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		authors = cursor.fetchall()

	return render_template("authors.html", authors = authors)

def delete_author(author_id):

	statement = '''
		DELETE FROM AUTHORS
		WHERE (ID = %d)
	''' % (int(author_id))

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)

	return redirect(url_for("authors_page"))
