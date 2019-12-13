from flask import Flask,render_template
from server import app,url
from flask import request, redirect, url_for
import psycopg2 as dbapi2
from book import book
from author import author
from closet import closet
from student import student
import time


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
			
			elif request.form["form_name"] == "filter": # FILTER FORM SUBMITTED

				statement = '''
					SELECT * FROM BOOKS
				'''
				
				where = False
				condition = []
				
				if request.form["book_name"]:
					condition.append("(NAME = '%s')" % (request.form["book_name"]))
				
				#if request.form["author_name"]:
				#	condition.append("()")
				
				if len(condition):
					
					if where == False:
						statement += " WHERE "
					last = len(condition) - 1
					t = 0
					for cond in condition:
						statement += cond
						if t != last:
							statement += " AND "
						t += 1
				
				genre_cond = request.form.getlist('genre')
				
				genre_statement = ""
				
				
				if len(genre_cond):
					if where == False:
						statement += " WHERE "
					first = True
					for item in genre_cond:
						if first == False:
							genre_statement += " OR "
						first = False
						genre_statement += "GENRE = " + "\'%s\'" % (str(item))
						
				if len(condition):
					statement += " AND "
				statement += "(" + genre_statement + ")" 
				
				
				# final statement
				print(statement)
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)
					books = cursor.fetchall()

				return render_template("admin_books.html", books = books, book_count = len(books))

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
	
		authors = request.form["authors"];
			
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute("select * from books")
			books = cursor.fetchall()
		print(books)
		return render_template("admin_books.html",books = books)


def book_page(book_id):
	print("in book_page")
	book = []
	authors = []
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
	print("testastastsat")
	print("book = ")
	print(book)
	print("authors = ")
	print(authors)
			
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
	books = []
	
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
		author_book = cursor.fetchall() # return book ids
				
		for row in author_book:
			print("row= ")
			print(row)
			book_id = row[0]
				
			print("book_id = " + str(book_id))
					
			statement_book_ids = '''
				SELECT * FROM BOOKS
				WHERE (ID = %d)
			''' % (int(book_id))
			
			cursor.execute(statement_book_ids)
			
			book = cursor.fetchall()
			
			print(book)			
			books.append(book)
		
	print("books = " + str(books))
	return render_template("author.html", author = author, books = books)	

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

	closets = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM CLOSETS")
		closets = cursor.fetchall()

	if request.method == "GET":
		return render_template("closets.html", closets = closets)
	else:
		tmpcloset = closet(request.form["closet_floor"], request.form["closet_block"] ,request.form["closet_number"], request.form["closet_type"], request.form["closet_size"], request.form["return_hour"])
		tmpcloset.add_to_db(url)

		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM CLOSETS")
			closets = cursor.fetchall()
		print(closets)
		return render_template("closets.html",closets = closets)

def admin_students():
	students = []	
	if request.method == "POST":
		tmp_student = student(request.form["name"], request.form["last_name"] ,request.form["faculty"], request.form["department"], request.form["grade"], time.time())
		tmp_student.add_to_db(url)
		
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM STUDENTS")
		students = cursor.fetchall()	
		
	return render_template("admin_students.html", students = students)

def admin_student(student_id):
	student = []
	books = []
	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute('''
			SELECT * FROM STUDENTS
			WHERE (ID = %d)
			''' % (int(student_id))
		)
		student = cursor.fetchall()	
		
		if(len(student)):
			student_id = student[0][0]
		
			cursor.execute('''
				SELECT * FROM STUDENT_BOOKS
				WHERE (STUDENT_ID = %d)
			''' % (int(student_id))
			)
			books = cursor.fetchall()
	
		cursor.execute('''
			SELECT * FROM BOOKS
			WHERE (COUNT > 0)
		'''
		)
		opt = cursor.fetchall()
		options = []
		#deleting unnecessary colmuns
		for op in opt:
			options.append(op[1])
		
	
	return render_template("student.html", student = student, lend_books = books , options = options)

def admin_login_page():
    return render_template("admin_login.html")
