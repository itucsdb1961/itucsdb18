url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template, session, abort

class author:
	def __init__(self,
				name,
				last_name,
				birth_year = "",
				birth_place = "",
				last_book_date = "",
				last_book_name = "",
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

	if not "access_level" in session or session["access_level"] > 2: # non-admin-user trying url manually / abort
		abort(451)

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

			elif request.form["form_name"] == "checkbox_filter":

				checkbox_cond = request.form.getlist("author_key")

				statement_delete = "DELETE FROM AUTHORS WHERE "
				update_statement = ""
				first = True
				for update in checkbox_cond:
					if not first:
						update_statement += " OR "
					update_statement += "ID = " + str(update)
					first = False

				# delete from book_authors relation
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute('''
						DELETE FROM BOOK_AUTHORS
						WHERE AUTHOR_ID = %d
					''' % (int(update)))


				statement_delete += update_statement

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement_delete)

	authors = []
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
		SELECT BOOK_ID FROM BOOK_AUTHORS
		WHERE (AUTHOR_ID = %d)
	''' % (int(author_id))

	with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute(statement_author)
			author = cursor.fetchall()[0]

			cursor.execute(statement_books)

			book_ids = cursor.fetchall()

			for book_id in book_ids:

				cursor.execute('''
					SELECT * FROM BOOKS
					WHERE ID = %d
				''' % (int(book_id[0])))

				books.append(cursor.fetchall()[0])

	print(books)

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
