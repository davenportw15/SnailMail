
class Mail:
	
	def __init__(self, db):
		self.db = db

	def create_mail(self, content, date_sent, sender, recipient, subject):
		cursor = self.db.cursor()
		cursor.execute("insert into mail (content, date_sent, sender, recipient, subject) values (?,?,?,?,?)",
				(content,
				date_sent,
				sender,
				recipient,
				subject) )
		self.db.commit()

	def get_mail(self, id):
		cursor = self.db.cursor()
		cursor.execute("select * from mail where id==?", (id,) )

	def get_mail_for_user(name):
		cursor.execute("select * from mail where recipient==?", (name,))
		mails = cursor.fetchall()
		return [
				{
					"content":omail[0],
					"date_sent":omail[1],
					"sender":omail[2],
					"recipient":omail[3],
					"subject":omail[4],
				}
			] for omail in mails

		








