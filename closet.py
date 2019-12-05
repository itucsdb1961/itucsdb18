import psycopg2 as dbapi2

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
