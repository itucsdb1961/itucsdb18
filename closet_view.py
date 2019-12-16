url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template, session

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
	if not "access_level" in session or session["access_level"] > 2: # non-admin-user trying url manually / abort
		abort(451)

	closets = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM CLOSETS")
		closets = cursor.fetchall()

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "checkbox_filter":

				checkbox_cond = request.form.getlist("closet_key")

				statement = "DELETE FROM CLOSETS WHERE "
				update_statement = ""
				first = True
				for update in checkbox_cond:
					if not first:
						update_statement += " OR "
					update_statement += "ID = " + str(update)
					first = False

				statement += update_statement

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)
					cursor.execute("SELECT * FROM CLOSETS")
					closets = cursor.fetchall()

				return render_template("admin_closets.html",closets = closets)

			elif request.form["form_name"] == "closet_create":
				tmpcloset = closet(request.form["closet_floor"], request.form["closet_block"] ,request.form["closet_number"], request.form["closet_type"], request.form["closet_size"], request.form["return_hour"])
				tmpcloset.add_to_db(url)

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute("SELECT * FROM CLOSETS")
					closets = cursor.fetchall()

			elif request.form["form_name"] == "filter":
				statement = '''
					SELECT * FROM CLOSETS
				'''

				where = False
				condition = []

				if request.form["floor"]:
					condition.append("(CLOSET_FLOOR ~* '.*" + str(request.form["floor"]) + ".*')")

				if request.form["closet_number"]:
					condition.append("(CLOSET_NUMBER ~* '.*" + str(request.form["closet_number"]) + ".*')")

				if request.form["closet_size"]:
					condition.append("(SIZE ~* '.*" + str(request.form["closet_size"]) + ".*')")

				if len(condition):
					statement += " WHERE "

					first = True
					for cond in condition:
						if not first:
							statement += " AND "
						first = False
						statement += cond

				# final statement
				print("statement = " + statement)

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)
					closets = cursor.fetchall()
				return render_template("admin_closets.html",closets = closets)

	return render_template("admin_closets.html",closets = closets)


def closets_page():

	closets = []

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM CLOSETS")
		closets = cursor.fetchall()

	if request.method == "POST":

		if request.form["form_name"] == "filter":
			statement = '''
				SELECT * FROM CLOSETS
			'''

			where = False
			condition = []

			if request.form["floor"]:
				condition.append("(CLOSET_FLOOR ~* '.*" + str(request.form["floor"]) + ".*')")

			if request.form["closet_number"]:
				condition.append("(CLOSET_NUMBER ~* '.*" + str(request.form["closet_number"]) + ".*')")

			if request.form["closet_size"]:
				condition.append("(SIZE ~* '.*" + str(request.form["closet_size"]) + ".*')")

			if len(condition):
				statement += " WHERE "

				first = True
				for cond in condition:
					if not first:
						statement += " AND "
					first = False
					statement += cond

			# final statement
			print("statement = " + statement)

			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				cursor.execute(statement)
				closets = cursor.fetchall()

	return render_template("closets.html", closets = closets)

def closet_page(closet_id):

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "closet_update":

				updates = []

				if request.form["floor"]:
					updates.append("CLOSET_FLOOR = " + str(request.form["floor"]))

				if request.form["block"]:
					updates.append("BLOCK = '" + str(request.form["block"]) + "'")

				if request.form["closet_number"]:
					updates.append("CLOSET_NUMBER = '" + str(request.form["closet_number"]) + "'")

				if request.form["closet_type"]:
					updates.append("CLOSET_TYPE = '" + str(request.form["closet_type"]) + "'")

				if request.form["size"]:
					updates.append("SIZE = '" + str(request.form["size"]) + "'")

				if request.form["return_hour"]:
					updates.append("RETURN_HOUR = '" + str(request.form["return_hour"]) + "'")

				if len(updates):

					statement = "UPDATE CLOSETS SET "

					update_statement = ""
					first = True
					for update in updates:
						if not first:
							update_statement += " , "
						update_statement += update
						first = False

					statement += update_statement

					where_statement = ''' WHERE ID = %d
								''' % (int(closet_id))

					statement += where_statement

					with dbapi2.connect(url) as connection:
						cursor = connection.cursor()
						cursor.execute(statement)

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute('''
						SELECT * FROM CLOSETS
						WHERE ID = %d
					   '''	% (int(closet_id)))
		closet = cursor.fetchall()[0]

	return render_template("closet.html",closet = closet)
