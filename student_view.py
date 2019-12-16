url = "postgres://mrzogiikkbrxmf:b6042668a00f9ea7e4d353f06e02e8c5ffab90a6a2a76191de8597340a254d68@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/dsbe8b5jahoaq"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template
import time

class student:
	def __init__(self,
				student_num,
				name,
				last_name,
				faculty,
				department,
				grade,
				membership_start_date,
				debt = 0):
		self.student_num = student_num
		self.name = name
		self.last_name = last_name
		self.faculty = faculty
		self.department = department
		self.grade = grade
		self.membership_start_date = membership_start_date
		self.debt = debt

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					STUDENTS (STUDENT_NUM, NAME, LAST_NAME, FACULTY, DEPART, GRADE, MEM_DATE, DEBT)
					VALUES 	('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%f')
					ON CONFLICT(STUDENT_NUM) DO NOTHING
					''' % (self.student_num, self.name, self.last_name, self.faculty, self.department, self.grade, self.membership_start_date, self.debt)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			cursor.close()

	def get_book_id(self, url):
		return False

def admin_students():

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "add_student":
				tmp_student = student(request.form["student_num"], request.form["name"], request.form["last_name"], request.form["faculty"], request.form["department"], request.form["grade"], time.time())
				tmp_student.add_to_db(url)
			elif request.form["form_name"] == "filter":

				condition = []

				if request.form["student_name"]:
					condition.append("(NAME ~* '.*" + str(request.form["student_name"]) + ".*')")

				if request.form["student_surname"]:
					condition.append("(LAST_NAME ~* '.*" + str(request.form["student_surname"]) + ".*')")

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

			elif request.form["form_name"] == "checkbox_filter":

				checkbox_cond = request.form.getlist("student_key")

				statement = "DELETE FROM STUDENTS WHERE "
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

	students = []
	statement = "SELECT * FROM STUDENTS"				

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(statement)
		students = cursor.fetchall()

	return render_template("admin_students.html", students = students)

def admin_student(student_id):
	student = []
	books = []

	if request.method == "POST":
		if "form_name" in request.form:
			if request.form["form_name"] == "update_student":

				updates = []

				if request.form["name"]:
					updates.append("NAME = '" + str(request.form["name"]) + "'")

				if request.form["last_name"]:
					updates.append("LAST_NAME = '" + str(request.form["last_name"]) + "'")

				if request.form["faculty"]:
					updates.append("FACULTY = '" + str(request.form["faculty"]) + "'")

				if request.form["department"]:
					updates.append("DEPART = '" + str(request.form["department"]) + "'")

				if request.form["grade"]:
					updates.append("GRADE = '" + str(request.form["grade"]) + "'")

				if request.form["debt"]:
					updates.append("DEBT = " + str(request.form["debt"]))

				statement = "UPDATE STUDENTS SET "

				update_statement = ""
				first = True
				for update in updates:
					if not first:
						update_statement += " , "
					first = False
					update_statement += update

				statement += update_statement

				where_statement = '''
					WHERE ID = %d
				''' % (int(student_id))

				statement += where_statement

				with dbapi2.connect(url) as connection:
					cursor = connection.cursor()
					cursor.execute(statement)

	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute('''
			SELECT * FROM STUDENTS
			WHERE ID = %d
		''' % (int(student_id)))
		student = cursor.fetchall()

	return render_template("student.html", student = student)
