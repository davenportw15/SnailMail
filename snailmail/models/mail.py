from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from datetime import timedelta
from snailmail.models.distance import time
from snailmail.models.distance import dist
from snailmail.database import Base
from snailmail.models.user import User

class Mail(Base):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key = True, nullable=False)
    subject = Column(String)
    content = Column(Text)
    date_sent = Column(DateTime,nullable=False)
    date_deliver = Column(DateTime,nullable=False)
    sender_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    recipient_id = Column(Integer,ForeignKey('users.id'),nullable=False)

    sender = relationship('User',foreign_keys=[sender_id])
    recipient = relationship('User',foreign_keys=[recipient_id])


    def __init__(self, subject, content, date_sent,
            sender_id, recipient_id):
        self.subject = subject
        self.content = content
        self.date_sent = date_sent
        self.sender_id = sender_id
        self.recipient_id = recipient_id

        self.sender = User.query.filter_by(id=sender_id).first();
        self.recipient = User.query.filter_by(id=recipient_id).first();



    def set_delay(self):
        print(self.sender)
        print(self.recipient)

        self.date_deliver = self.date_sent +\
                timedelta(
                days=time(
                    dist(self.sender.latitude,
                        self.sender.longitude,
                        self.recipient.latitude,
                        self.recipient.longitude)
                    ))
        print(self.date_deliver)



    def __repr__(self):
        return '<Mail %d, subject=%r>' % (self.id,self.subject)
    
    def serialize(self):
        return {
                    "content":self.content,
                    "date_sent":self.date_sent,
                    "sender_id":self.sender_id,
                    "recipient_id":self.recipient_id,
                    "sender_name":self.recipient.username,
                    "subject":self.subject,
                    "id":self.id,
                    "deliver_date":self.date_deliver
                }
