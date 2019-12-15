url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"

import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template
from random import randint

class shelf:
	def __init__(self,
				num,
				block,
				floor,
				capacity,
				book_genre = None):
		self.num = num
		self.block = block
		self.floor = floor
		self.capacity = capacity
		self.book_genre = book_genre

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					SHELVES	(NUM, BLOCK, FLR, BOOK_GENRE, CAPACITY)
					VALUES 	(%d, %d, %d, '%s', %d)
					ON CONFLICT(NUM, BLOCK, FLR) DO NOTHING
					''' % (self.num, self.block, self.floor, self.book_genre, self.capacity)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			connection.commit()


def admin_shelves_page():
	shelves = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("select * from shelves")
		shelves = cursor.fetchall()

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "add_shelve": # add shelve FORM SUBMITTED
				tmp_shelve = shelf(request.form["num"], request.form["block"] ,request.form["floor"],  request.form["capacity"], request.form["genre"])
				tmp_shelve.add_to_db(url)

				# collect and serve
				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute("select * from shelves")
					shelves = cursor.fetchall()

			elif request.form["form_name"] == "filter": # add shelve FORM SUBMITTED

				statement = '''
					SELECT * FROM SHELVES
				'''

				cond = []

				if request.form["type"]:
					cond.append('''
						(TYPE = '%s')
						''' % (str(request.form["type"]))
					)
				if request.form["capacity"]:
					st = str(request.form["capacity"])
					cnd = ""

					if st.last == '+':
						val = int(st[0:-2])
						cnd = '''
							(CAPACITY > %d)
						''' % (val)
						cond.append(cnd)
					else:
						cond.append('''
							(CAPACITY = %d)
						''' % (int(request.form["capacity"]))
						)

				if len(cond):

					statement += " WHERE "

					first = True
					for cnd in cond:
						if not first:
							statement += " AND "
						first = False
						statement += cnd

				cursor.execute(statement)
				shelves = cursor.fetchall()

			elif request.form["form_name"] == "random":

				num = randint(1,10)
				block = randint(1,5)
				floor  = randint(0,3)
				capacity = 250
				genre = randint(0,3)

				genres = ["horror","sci-fi","fantasy", "romance"]

				tmp_shelve = shelf(num,block,floor,capacity,genres[genre])
				tmp_shelve.add_to_db(url)

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute("select * from shelves")
					shelves = cursor.fetchall()
				
	return render_template("admin_shelves.html", shelves = shelves, shelf_count = len(shelves))
	
def shelf_page(shelf_id):
	print("in shelf_page")
	shelf = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute('''
				select * from shelves
				where ID = %d
				''' % (int(shelf_id)))
		shelf = cursor.fetchall()
	return render_template("shelf.html", shelf = shelf)
