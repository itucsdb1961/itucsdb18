url = "postgres://vzvhmhqevlcedf:141b03607dee6c5c995d91b952b06e4fc122006f5cd2c1d789403aae34dc40a1@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dafo7esm4hjfc7"
secret_key = "hjkalsfdlamfrqwrxzc"
import psycopg2 as dbapi2
from flask import Flask, request, redirect, url_for,render_template

class student:
	def __init__(self,
				name,
				last_name,
				faculty,
				department,
				grade,
				membership_start_date,
				debt = 0):
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
					STUDENTS (NAME, LAST_NAME, FACULTY, DEPART, GRADE, MEM_DATE, DEBT) 
					VALUES 	('%s', '%s', '%s', '%s', '%s', '%s', '%f')
					ON CONFLICT(NAME,LAST_NAME,FACULTY,DEPART,GRADE) DO NOTHING
					''' % (self.name, self.last_name, self.faculty, self.department, self.grade, self.membership_start_date, self.debt)
				
		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			cursor.close()
	
	def get_book_id(self, url):
		return False
					
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
	
	if request.method == "POST":
		
		if(request.form["form_name"] == "book_selector"):
			
			selected_book = str(request.form["options"])
			#print(request.form["options"])
			
			#get book_id
			ids = []
			
			statement = '''
				SELECT * FROM BOOKS
				WHERE (NAME= '%s')
			''' % (selected_book)
			
			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				cursor.execute(statement)
				ids = cursor.fetchall()
				
				book_id = int(ids[0][0])
				
				relation_insert_statement = '''
					INSERT INTO 
					STUDENT_BOOKS (BOOK_ID, STUDENT_ID, DATE_LEND) 
					VALUES 	(%d, %d, %f)
					ON CONFLICT(BOOK_ID, STUDENT_ID) DO NOTHING
				''' % (book_id, int(student_id), time.time())
				
				cursor.execute(relation_insert_statement)
				
				#update book_count
				
				book_update_statement = '''
					UPDATE BOOKS
					SET COUNT = COUNT-1
					WHERE (ID = %d)
				''' % (book_id)
				
				cursor.execute(book_update_statement)
				
			
			
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
			
			books_rel = cursor.fetchall()
			
			for r in books_rel:
				
				bk_id = int(r[0]) 
				
				statement = '''
					SELECT ID,NAME FROM BOOKS
					WHERE (ID = %d)					
				''' % (bk_id)
				
				cursor.execute(statement)
				
				books = cursor.fetchall()
				
			print("books = " + str(books))
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
