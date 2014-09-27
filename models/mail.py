from datetime import datetime

class Mail:
	
	def __init__(self, db):
		self.db = db

	def create_mail(self, content, date_sent, deliver_date, sender, recipient, subject):
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
		cursor.execute("select content, date_sent, sender, recipient, subject from mail where id==?", (id,) )
		mail = cursor.fetchone()
		return {
					"content":mail[0],
					"date_sent":mail[1],
					"sender":mail[2],
					"recipient":mail[3],
					"subject":mail[4],
					"id":mail[5]
				}

	def get_mail_for_user(self, name):
		cursor = self.db.cursor()
		cursor.execute("select content, date_sent, sender, recipient, subject, id from mail where recipient==?", (name,))
		mails = cursor.fetchall()
		return [
				{
					"content":omail[0],
					"date_sent":omail[1],
					"sender":omail[2],
					"recipient":omail[3],
					"subject":omail[4],
					"id":omail[5]
				}
			 for omail in mails]
