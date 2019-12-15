url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template
from author_view import author

class book:
	def __init__(self,
				name,
				pub_year,
				lang = None,
				genre = None,
				pub_location = None,
				publisher = None):
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
			return ids[0][0]


def admin_books_page():
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
								VALUES 	('%s', '%s')
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
						statement += cond

				# final statement
				print("statement = " + statement)
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)
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
					condition.append("(NAME ~* '^" + str(request.form["book_name"]) + "*')")

				if request.form["genre"]:
					condition.append("(GENRE ~* '^" + str(request.form["genre"]) + "*')")

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
					books = cursor.fetchall()

	return render_template("books.html", books = books)

def book_page(book_id):
	print("in book_page")
	book = []
	authors = []

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

				statement = "UPDATE BOOKS SET "

				update_statement = ""
				first = True
				for update in updates:
					if not first:
						update_statement += " , "
					update_statement += update

				statement += update_statement

				where_statement = '''
					WHERE ID = %d
				''' % (int(book_id))

				statement += where_statement

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)

	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(
				'''
				select * from books
				where ID = %d
				''' % (int(book_id))
				)
		book = cursor.fetchall()
		cursor.execute(
			'''
				select * from BOOK_AUTHORS
				where BOOK_ID = %d
			''' % (int(book_id))
		)
		rows = cursor.fetchall()

		print("rows = ")
		print(rows)

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

	return render_template("book.html", book = book , authors = authors)

def delete_book(book_id):

	print("book_id = ")
	print(book_id)

	statement = '''
		DELETE FROM BOOKS
		WHERE (ID = %d)
	''' % (int(book_id))

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)

	return redirect(url_for("books_page"))
