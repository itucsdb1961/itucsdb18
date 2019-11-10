from flask import Flask,render_template
from server import app,url

import psycopg2 as dbapi2
from book import book

@app.route("/")
def home_page():
	
	tmpbook = book("the fall", 1956)
	tmpbook.add_to_db(url)
	
	
	
	return render_template("home.html")

@app.route("/books")
def books_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		rows = cursor.fetchall()
		for r in rows:
			print(r)	
		cursor.close()
	#print(url)
	
	
	
	return render_template("books.html")

@app.route("/")
def authors_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("delete from books")
		cursor.close()
	#print(url)
	
	
	
	return render_template("authors.html")
    
@app.route("/")
def closets_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("drop table books")
		cursor.close()
		
		
	return render_template("closets.html")

@app.route("/")
def admin_login_page():
    return render_template("admin_login.html") 
