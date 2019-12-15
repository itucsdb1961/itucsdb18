url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template

class closet:
	def __init__(self,
				floor,
				block,
				number,
				closet_type,
				size,
				return_hour):
		self.floor = floor
		self.block = block
		self.number = number
		self.closet_type = closet_type
		self.size = size
		self.return_hour = return_hour

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					CLOSETS	(CLOSET_FLOOR, BLOCK, CLOSET_NUMBER, CLOSET_TYPE, SIZE, RETURN_HOUR)
					VALUES 	('%s', '%s', '%s', '%s', '%s', '%s')
					ON CONFLICT(CLOSET_FLOOR,CLOSET_NUMBER) DO NOTHING
					''' % (self.floor, self.block, self.number, self.closet_type, self.size, self.return_hour)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			connection.commit()

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

def closet_page(closet_id):

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute('''
						SELECT * FROM CLOSETS
						WHERE ID = %d
					   '''	% (int(closet_id)))
		closet = cursor.fetchall()
	return render_template("closet.html",closet = closet)
