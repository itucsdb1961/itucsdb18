from flask import Flask, request, redirect, url_for, session, render_template
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


def admin_signup_page():
	
	if request.method == "POST":
		
		
		
		if request.form["form_name"] == "signup":
			
			username = str(request.form["username"])
			password = str(request.form["password"])
			password2 = str(request.form["password_again"])
			
			h_password = md5(password.encode('utf-8')).hexdigest()
			h_password2 = md5(password2.encode('utf-8')).hexdigest() 
			print(h_password)
			print(h_password2)
			if not h_password == h_password2:
				return redirect(url_for("admin_signup_page"))

			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				cursor.execute('''
					SELECT * FROM USERS
					WHERE (USERNAME = '%s')
					''' % (username)
				)
				users = cursor.fetchall()
				print(len(users))
				if len(users):	
					return redirect(url_for("admin_signup_page"))
				
				add_user_statement = '''
					INSERT INTO 
					USERS (USERNAME, H_PASSWORD) 
					VALUES 	('%s', '%s') 
				'''% (username, h_password)
				
				cursor.execute(add_user_statement)
				
				print("added user")
				return redirect(url_for("admin_login_page"))
				
	return render_template("admin_signup.html")
	
def admin_login_page():
	
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM USERS")
		
		users = cursor.fetchall()
		
		print(users)
		
		
	print("in Login funct")
	
	if request.method == "POST":
		
		print("in POST")
		
		if request.form["form_name"] == "login":
			
			username = str(request.form["username"])
			password = str(request.form["password"])
			
			print(username)
			print(password)
			
			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				cursor.execute('''
					SELECT * FROM USERS
					WHERE (USERNAME = '%s')
					''' % (username)
				)
				users = cursor.fetchall()
				print(len(users))
				if len(users) == 0:
					print("user does not exist")
					return redirect(url_for("admin_login_page", error = "Invalid Username"))
				else:
					h_password = md5(password.encode('utf-8')).hexdigest()
					print("h_password = " + h_password)
					for user in users:
						
						print("user = ")
						print(user[2])
						
						if(h_password == user[2]):# succesfull login
							print("success")
							session["logged_in"] = True
							session["username"] = str(user[1])
							session["password"] = str(user[2])
							return redirect(url_for("admin_logged_page"))
						else:
							return redirect(url_for("admin_login_page", error = "Wrong password"))
				#cursor.execute(add_user_statement)
		else:
			print("kek")
					
	return render_template("admin_login.html")
	
def admin_logged_page():
	
	return render_template("admin_logged.html")
