from flask import Flask,render_template
from server import app,url
from flask import request, redirect, url_for
import psycopg2 as dbapi2
from book import book

@app.route("/")
def home_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		row = cursor.fetchall()
		for r in row:
			print(r)
	return render_template("home.html")

@app.route("/books")
def books_page():

	if request.method == "GET":
		return render_template("books.html")
	else:
		tmpbook = book(request.form["book_name"], request.form["pub_year"] ,request.form["book_lang"], request.form["book_genre"], request.form["pub_location"], request.form["publisher"])
		tmpbook.add_to_db(url)
		return render_template("books.html")

@app.route("/")
def authors_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("delete from books")
	#print(url)



	return render_template("authors.html")

@app.route("/")
def closets_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("drop table books")


	return render_template("closets.html")

@app.route("/")
def admin_login_page():
    return render_template("admin_login.html")
