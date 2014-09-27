from datetime import datetime
from distance import time
from distance import dist

class Mail:
	
	def __init__(self, db, users):
		self.db = db
		self.users = users

	def create_mail(self, content, date_sent, sender, recipient, subject):
		cursor = self.db.cursor()
		u_cursor = self.users.cursor()

		u_cursor.execute("select latitude, longitude where username==?", (sender,))
		sender_coords = u_cursor.fetchall()
		u_cursor.execute("select latitude, longitude where username==?", (recipient,))
		recipient_coords = u_cursor.fetchall()

		delay = time(dist(sender_coords[0],sender_coords[1],recipient_coords[0],recipient_coords[1]))

		deliver_date= datetime.strptime(date_sent,"%Y-%m-%d") + datetime.timedelta(days=delay)



		cursor.execute("insert into mail (content, date_sent, deliver_date, sender, recipient, subject) values (?,?,?,?,?)",
				(content,
				date_sent,
				deliver_date,
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
