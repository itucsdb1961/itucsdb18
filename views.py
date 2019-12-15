from flask import Flask,render_template
from server import app,url
import psycopg2 as dbapi2
from book import book
from author import author
from closet import closet
from student import student
import time

from hashlib import md5

def home_page():
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from books")
		row = cursor.fetchall()
		for r in row:
			print(r)
	return render_template("home.html")



def admin_closets_page():
	# with dbapi2.connect(url) as connection:
	# 	cursor = connection.cursor()
	# 	cursor.execute("drop table authors")

	closets = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM CLOSETS")
		closets = cursor.fetchall()

	if request.method == "GET":
		return render_template("admin_closets.html", closets = closets)
	else:
		tmpcloset = closet(request.form["closet_floor"], request.form["closet_block"] ,request.form["closet_number"], request.form["closet_type"], request.form["closet_size"], request.form["return_hour"])
		tmpcloset.add_to_db(url)

		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM CLOSETS")
			closets = cursor.fetchall()
		print(closets)
		return render_template("admin_closets.html",closets = closets)


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




def admin_login_page():
	
	if request.method == "POST":
		
		if request.form["form_name"] == "login":
			
			username = str(request.form["username"])
			password = str(request.form["password"])
			
			is_username_taken = False
			
			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				cursor.execute('''
					SELECT * FROM USERS
					WHERE (USERNAME = '%s')
					''' % (username)
				)
				q = cursor.fetchall()
				if len(q) > 0:
					redirect(url_for("admin_login_page"))
					
				h_password = md5(request.form.get('password').encode('utf-8')).hexdigest()
				
				add_user_statement = '''
					INSERT INTO 
					STUDENTS (USERNAME, H_PASSWORD) 
					VALUES 	('%s', '%s)
				''' % (username, h_password)
				
				cursor.execute(add_user_statement)
					
	return render_template("admin_login.html")
