url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"

from flask import Flask, request, redirect, url_for, session, render_template
import psycopg2 as dbapi2
import time

from hashlib import md5

def home_page():
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
						INSERT INTO 
						USERS (USERNAME, H_PASSWORD)
						VALUES ('%s', '%s')
					''' % (username, password)
					)

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
				if not len(users):
					print("user does not exist")
					return redirect(url_for("admin_login_page", error = "Invalid Username"))
				else:
					h_password = md5(password.encode('utf-8')).hexdigest()
					print("h_password = " + h_password)
					for user in users:
						
						print("user = ")
						print(user[2])
						
						if(h_password == md5(user[2].encode('utf-8')).hexdigest()):# succesfull login
							print("success")
							session["logged_in"] = True
							session["username"] = str(user[1])
							session["password"] = str(user[2])
							session["access_level"] = int(user[3])
							return redirect(url_for("admin_logged_page"))
						else:
							return redirect(url_for("admin_login_page", error = "Wrong password"))
				#cursor.execute(add_user_statement)
	return render_template("admin_login.html")
	
def admin_logged_page():
	
	return render_template("admin_logged.html")
