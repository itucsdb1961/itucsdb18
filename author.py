
import psycopg2 as dbapi2

class author:
	def __init__(self,
				name,
				last_name,
				birth_year = None,
				birth_place = None,
				last_book_date = None,
				last_book_name = None,
				):
		self.name = name
		self.last_name = last_name
		self.birth_year = birth_year
		self.birth_place = birth_place
		self.last_book_date = last_book_date
		self.last_book_name = last_book_name

	def add_to_db(self,db_url):
		STATEMENT ='''
					INSERT INTO
					AUTHORS	(NAME, LAST_NAME, BIRTH_YR, BIRTH_PLACE, LAST_BOOK_DATE, LAST_BOOK_NAME)
					VALUES 	('%s', '%s', '%s', '%s', '%s', '%s')					
					ON CONFLICT(NAME, LAST_NAME) DO NOTHING
					''' % (self.name, self.last_name, self.birth_year, self.birth_place, self.last_book_date, self.last_book_name)

		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(STATEMENT)
			connection.commit()
	
	def fetch_id(self,db_url):
		
		with dbapi2.connect(db_url) as connection:
			cursor = connection.cursor()
			cursor.execute(
					'''
					select * from authors
					where 
					NAME = '%s' and
					LAST_NAME = '%s'
					''' % (self.name, self.last_name)
					)
			ids = cursor.fetchall()
			return ids[0][0]

		
