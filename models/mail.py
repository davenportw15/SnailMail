from sqlalchemy import *

class Mail:
	
	def __init__(self, metadata):
		self.metadata = metadata
		self.table = Table('mail', metadata,
				Column('id',Integer, primary_key=True)
				Column('content', String),
				Column('date_sent', Date),
				Column('sender', String),
				Column('recipient', String),
				Column('subject', String),
				)
