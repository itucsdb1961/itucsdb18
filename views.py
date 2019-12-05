from flask import Flask,render_template
from server import app,url
from flask import request, redirect, url_for
import psycopg2 as dbapi2
from book import book
from author import author

def home_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		row = cursor.fetchall()
		for r in row:
			print(r)
	return render_template("home.html")

def books_page():
	books = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		books = cursor.fetchall()

#	if request.method == "GET":
#		return render_template("books.html")
#	else:
#		tmpbook = book(request.form["book_name"], request.form["pub_year"] ,request.form["book_lang"], request.form["book_genre"], request.form["pub_location"], request.form["publisher"])
#		tmpbook.add_to_db(url)
#		return render_template("books.html")

	if request.method == "GET":
		print(books)
		return render_template("admin_books.html", books = books)
	else:
		tmpbook = book(request.form["book_name"], request.form["pub_year"] ,request.form["book_lang"], request.form["book_genre"], request.form["pub_location"], request.form["publisher"])
		tmpbook.add_to_db(url)

		print(tmpbook)
		print(books)

		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute("select * from books")
			books = cursor.fetchall()

		return render_template("admin_books.html", books = books)

def admin_books_page():

	books = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		books = cursor.fetchall()

	if request.method == "GET":
		return render_template("admin_books.html", books = books)
	else:
		tmpbook = book(request.form["book_name"], request.form["pub_year"] ,request.form["book_lang"], request.form["book_genre"], request.form["pub_location"], request.form["publisher"])
		tmpbook.add_to_db(url)

		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute("select * from books")
			books = cursor.fetchall()
		print(books)
		return render_template("admin_books.html",books = books)



def book_page(book_id):
	
	book = []
	
	statement = '''
		SELECT * FROM BOOKS
		WHERE (ID = %d)
	''' % (int(book_id))
	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		book = cursor.fetchall()
	
	return render_template("book.html", book = book)
	
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


def authors_page():

	if request.method == "POST":
		tmp_author = author(request.form["author_name"], request.form["last_name"] ,request.form["birth_year"], request.form["birth_place"], request.form["last_book_date"], request.form["last_book_name"])
		tmp_author.add_to_db(url)

	authors = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from authors")
		authors = cursor.fetchall()
	return render_template("authors.html", authors = authors)
	
def author_page(author_id):
	
	author = []
	
	statement = '''
		SELECT * FROM AUTHORS
		WHERE (ID = %d)
	''' % (int(author_id))
	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		author = cursor.fetchall()
	
	return render_template("author.html", author = author)	

def delete_author(author_id):
	
	statement = '''
		DELETE FROM AUTHORS
		WHERE (ID = %d)
	''' % (int(author_id))
	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
	
	return redirect(url_for("authors_page"))

def closets_page():
	# with dbapi2.connect(url) as connection:
	# 	cursor = connection.cursor()
	# 	cursor.execute("drop table authors")


	return render_template("closets.html")

def admin_login_page():
    return render_template("admin_login.html")
