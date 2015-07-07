from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from datetime import timedelta
from snailmail.models.distance import time
from snailmail.models.distance import dist
from snailmail.database import Base

class Mail(Base):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key = True, nullable=False)
    subject = Column(String)
    content = Column(Text)
    date_sent = Column(DateTime,nullable=False)
    date_deliver = Column(DateTime,nullable=False)
    sender_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    recipient_id = Column(Integer,ForeignKey('users.id'),nullable=False)

    def __init__(self, subject, content, date_sent,
            sender_id, recipient_id):
        self.subject = subject
        self.content = content
        self.date_sent = date_sent
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.date_deliver = self.date_sent + timedelta(days=0)

        self.sender = relationship('Users',foreign_keys=[sender_id])
        self.recipient = relationship('Users',foreign_keys=[recipient_id])


    def __repr__(self):
        return '<Mail %d, subject=%r>' % (self.id,self.subject)
    
    def serialize(self):
        return {
                    "content":self.content,
                    "date_sent":self.date_sent,
                    "sender_id":self.sender_id,
                    "recipient_id":self.recipient_id,
                    "subject":self.subject,
                    "id":self.id,
                    "deliver_date":self.date_deliver
                }



"""    
    def __init__(self, db, users):
        self.db = db
        self.users = users

    def create_mail(self, content, date_sent, sender, recipient, subject):
        cursor = self.db.cursor()

        delay = time(dist(
            self.users.get_user_by_username(sender)["latitude"],
            self.users.get_user_by_username(sender)["longitude"],
            self.users.get_user(recipient)["latitude"],
            self.users.get_user(recipient)["longitude"]
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

    def get_mail_for_user(self, recipient_id):
        cursor = self.db.cursor()
        print("recipient_id: ",recipient_id)
        cursor.execute("select content, date_sent, sender, recipient, subject, id, deliver_date from mail where recipient==?", (recipient_id,))
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

        return list(filter(hasArrived, all_mail))
    """
