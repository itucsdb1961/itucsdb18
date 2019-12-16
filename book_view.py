url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template, session, abort
from author_view import author

class book:
	def __init__(self,
				name,
				pub_year,
				lang = "",
				genre = "",
				pub_location = "",
				publisher = ""):
		self.name = name
		self.pub_year = pub_year
		self.lang = lang
		self.genre = genre
		self.pub_location = pub_location
		self.publisher = publisher

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					BOOKS	(NAME, PB_YR, LANG, GENRE, PB_LOC, PUBLISHER)
					VALUES 	('%s', '%s', '%s', '%s', '%s', '%s')
					ON CONFLICT(NAME,PB_YR) DO NOTHING
					''' % (self.name, self.pub_year, self.lang, self.genre, self.pub_location, self.publisher)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			connection.commit()

	def fetch_id(self,db_url):

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(
					'''
					select * from books
					where
					NAME = '%s' and
					PB_YR = '%s'
					''' % (self.name, self.pub_year)
					)
			ids = cursor.fetchall()
			return int(ids[0][0])


def admin_books_page():

	if not "access_level" in session or session["access_level"] > 2: # non-admin-user trying url manually / abort
		abort(451)

	books = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		books = cursor.fetchall()

	if request.method == "GET":
		return render_template("admin_books.html", books = books, book_count = len(books))
	else:
		if "form_name" in request.form:
			if request.form["form_name"] == "book_create": # CREATE BOOK FORM SUBMITTED
				tmp_book = book(request.form["book_name"], request.form["pub_year"] ,request.form["book_lang"], request.form["book_genre"], request.form["pub_location"], request.form["publisher"])
				tmp_book.add_to_db(url)

				authors = request.form["authors"]
				authorList = authors.split('+')
				for author0 in authorList:
					parsed_name = author0.split(' ')

					last_name = parsed_name[-1]
					first_name = parsed_name[0]

					ct = len(parsed_name)
					t = 0
					for nm in parsed_name:
						if t==0 or t==ct-1:
							t+=1
						else:
							first_name +=  " " + nm
							t+=1

					tmp_author = author(str(first_name), str(last_name))
					tmp_author.add_to_db(url)

					# adding book-author relation
					STATEMENT ='''
								INSERT INTO
								BOOK_AUTHORS (BOOK_ID, AUTHOR_ID)
								VALUES 	(%d, %d)
								ON CONFLICT(BOOK_ID, AUTHOR_ID) DO NOTHING
								''' % (tmp_book.fetch_id(url), tmp_author.fetch_id(url))

					with dbapi2.connect(url) as connection:
						cursor = connection.cursor()
						cursor.execute( STATEMENT )

				# collect and serve
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute("select * from books")
					books = cursor.fetchall()

				return render_template("admin_books.html", books = books, book_count = len(books))

			elif request.form["form_name"] == "filter":

				statement = '''
					SELECT * FROM BOOKS
				'''

				where = False
				condition = []

				if request.form["book_name"]:
					condition.append("(NAME ~* '^" + str(request.form["book_name"]) + "*')")

				if request.form["genre"]:
					condition.append("(GENRE ~* '^" + str(request.form["genre"]) + "*')")

				if len(condition):
					statement += " WHERE "

					first = True
					for cond in condition:
						if not first:
							statement += " AND "
						first = False
						statement += cond

				# final statement
				print("statement = " + statement)
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)
					books = cursor.fetchall()

			elif request.form["form_name"] == "checkbox_filter":

				checkbox_cond = request.form.getlist("book_key")

				statement = "DELETE FROM BOOKS WHERE "
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
							WHERE BOOK_ID = %d
						''' % (int(update)))

				statement += update_statement

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)


	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		books = cursor.fetchall()

	return render_template("admin_books.html", books = books, book_count = len(books))

def books_page():

	books = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		books = cursor.fetchall()

	if request.method == "GET":
		return render_template("books.html", books = books)
	else:
		if "form_name" in request.form:
			if request.form["form_name"] == "filter":
				statement = '''
					SELECT * FROM BOOKS
				'''

				where = False
				condition = []

				if request.form["book_name"]:
					condition.append("(NAME ~* '.*" + str(request.form["book_name"]) + ".*')")

				if request.form["genre"]:
					condition.append("(GENRE ~* '.*" + str(request.form["genre"]) + ".*')")

				if len(condition):
					statement += " WHERE "

					first = True
					for cond in condition:
						if not first:
							statement += " AND "
						first = False
						statement += cond

				# final statement
				print("statement = " + statement)

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)
					books = cursor.fetchall()

	return render_template("books.html", books = books)

def book_page(book_id):
	book = []
	authors = []
	shelf = []

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "update":

				updates = []

				if request.form["pub_year"]:
					updates.append("PB_YR = " + str(request.form["pub_year"]))

				if request.form["book_lang"]:
					updates.append("LANG = '" + str(request.form["book_lang"]) + "'")

				if request.form["book_genre"]:
					updates.append("GENRE = '" + str(request.form["book_genre"]) + "'")

				if request.form["pub_location"]:
					updates.append("PB_LOC = '" + str(request.form["pub_location"]) + "'")

				if request.form["publisher"]:
					updates.append("PUBLISHER = '" + str(request.form["publisher"]) + "'")

				if len(updates):
					statement = "UPDATE BOOKS SET "
					update_statement = ""
					first = True
					for update in updates:
						if not first:
							update_statement += " , "
						update_statement += update
						first = False

					statement += update_statement

					where_statement = '''
						WHERE ID = %d
					''' % (int(book_id))

					statement += where_statement

					with dbapi2.connect(url) as connection:
						cursor = connection.cursor()
						cursor.execute(statement)

			elif request.form["form_name"] == "select_shelf":

				shelf_name = str(request.form["shelf_name"])

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute('''
						SELECT ID FROM SHELVES
						WHERE NAME = '%s'
					''' % (shelf_name)
					)

					shelf_id = int(cursor.fetchall()[0])

					cursor.execute('''
						INSERT INTO
						SHELF_BOOKS (BOOK_ID, SHELF_ID)
						VALUES 	(%d, %d)
						ON CONFLICT(BOOK_ID, AUTHOR_ID) DO NOTHING
					''' % (int(book_id), int(shelf_id))
					)



	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(
				'''
				select * from books
				where ID = %d
				''' % (int(book_id))
				)
		book = cursor.fetchall()[0]
		cursor.execute(
			'''
				select * from BOOK_AUTHORS
				where BOOK_ID = %d
			''' % (int(book_id))
		)
		rows = cursor.fetchall()

		for r in rows:
			author_id = int(r[1])

			cursor.execute(
				'''
					select * from AUTHORS
					where ID = %d
				''' % (author_id)
			)
			tmp_author = cursor.fetchall()[0]
			authors.append(tmp_author)

		cursor.execute(
		'''
			select * from SHELF_BOOKS
			where BOOK_ID = %d
		''' % (int(book_id))
		)

		shelf_id = int(cursor.fetchall()[0])

		cursor.execute(
		'''
			select * from SHELVES
			where ID = %d
		''' % (int(shelf_id))
		)

		shelf = cursor.fetchall()[0]

	return render_template("book.html", book = book , authors = authors, shelf = shelf)
