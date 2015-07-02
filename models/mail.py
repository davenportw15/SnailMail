from datetime import datetime
from datetime import timedelta
from models.distance import time
from models.distance import dist

class Mail:
	
	def __init__(self, db, users):
		self.db = db
		self.users = users

	def create_mail(self, content, date_sent, sender, recipient, subject):
		cursor = self.db.cursor()

		delay = time(dist(
			self.users.get_user_by_username(sender)["latitude"],
			self.users.get_user_by_username(sender)["longitude"],
			self.users.get_user_by_username(recipient)["latitude"],
			self.users.get_user_by_username(recipient)["longitude"]
		))

		deliver_date = datetime.strptime(date_sent,"%Y-%m-%d") + timedelta(days=delay)
		#print deliver_date


		cursor.execute("insert into mail (content, date_sent, deliver_date, sender, recipient, subject) values (?,?,?,?,?,?)",
				(content,
				date_sent,
				str((deliver_date).year) + "-" + str((deliver_date).month) + "-" + str((deliver_date).day),
				sender,
				recipient,
				subject) )
		self.db.commit()

	def get_mail(self, id):
		cursor = self.db.cursor()
		cursor.execute("select content, date_sent, sender, recipient, subject, deliver_date from mail where id==?", (id,) )
		mail = cursor.fetchone()
		return {
					"content":mail[0],
					"date_sent":mail[1],
					"sender":mail[2],
					"recipient":mail[3],
					"subject":mail[4],
					"id":mail[5],
					"deliver_date": mail[6]
				}

	def get_mail_for_user(self, name):
		cursor = self.db.cursor()
		cursor.execute("select content, date_sent, sender, recipient, subject, id, deliver_date from mail where recipient==?", (name,))
		mails = cursor.fetchall()
		all_mail = [
				{
					"content":omail[0],
					"date_sent":omail[1],
					"sender":omail[2],
					"recipient":omail[3],
					"subject":omail[4],
					"id":omail[5],
					"deliver_date": omail[6]
				}
			 for omail in mails]

		def hasArrived(mail):
			return not (datetime.now() < datetime.strptime(mail["deliver_date"], "%Y-%m-%d"))

		return filter(hasArrived, all_mail)
