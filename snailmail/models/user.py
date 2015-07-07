from sqlalchemy import Column, Integer, String, LargeBinary, \
        Float
from sqlalchemy.orm import relationship, backref
from snailmail.database import Base
from snailmail.models import secure_pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True,nullable=False,
            autoincrement=True)
    username = Column(String, unique=True,nullable=False)
    password_key = Column(LargeBinary,nullable=False)
    password_salt = Column(LargeBinary,nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, username, password,
            latitude, longitude):
        self.username = username
        sp = secure_pass.Password(password)
        self.password_key = sp.get_hash()
        self.password_salt = sp.get_salt()
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<User %r, id=%d>' % (self.username,self.id)

    def serialize(self):
        return {
                'id':self.id,
                'username':self.username,
                'password_key':self.password_key,
                'password_salt':self.password_salt,
                'latitude':self.latitude,
                'longitude':self.longitude
                }

    @staticmethod
    def unserialize(indict,db_session):
        return User.query.filter(User.id==indict['id']).first()

    @staticmethod
    def get_user(username, password, db_session):
        user = User.query.filter(User.username == username).first()
        if user is None:
            raise Exception("Login incorrect")
        if secure_pass.Password.check_pass(
                password,
                user.password_key,
                user.password_salt):
            return user
        raise Exception("Login incorrect")

    @staticmethod
    def get_user_by_username(username,db_session):
        return User.query.filter(User.username == username).first()



"""

  @staticmethod
  def user_exists(self, username, password):
    cursor = self.db.cursor()
    # get the count of users with that username. If the
    # count is greater than one, throw up. If it's zero,
    # return false. Otherwise, procede.
    cursor.execute("select count(id) num from users where username = ?",
            (username,))
    row = cursor.fetchone()
    assert row['num'] < 2
    if row['num'] < 1:
        return False


    # get the salt, key for the username
    cursor.execute("select password_salt, password_key from users where username == ?",
            (username,))
    row = cursor.fetchone()

    salt = row['password_salt']
    key = row['password_key']

    return secure_pass.Password.check_pass(
            password,
            key,
            salt
            )


  @staticmethod
  def get_user(self, id):
    cursor = self.db.cursor()
    cursor.execute(
      "select username, latitude, longitude, id from users where id == ?",
      (id,)
    )
    data = cursor.fetchone()
    return {
      "username": data[0],
      "latitude": data[1],
      "longitude": data[2],
      "id": data[3]
    }

  def get_user_by_username(self, username):
    cursor = self.db.cursor()
    print("username to get is: ",username)
    cursor.execute(
      "select username, latitude, longitude, id from users where username == ?",
      (username,)
    )
    data = cursor.fetchone()
    if data is None:
        raise Exception("No user" + username)
    return {
      "username": data[0],
      "latitude": data[1],
      "longitude": data[2],
      "id": data[3]
    }
    """
