class Users:

  def __init__(self, db):
    self.db = db

  def create_user(self, username, password, latitude, longitude):
    cursor = self.db.cursor()
    cursor.execute(
      "insert into users (username, password, latitude, longitude) values (?, ?, ?, ?)",
      (username,
      password,
      latitude,
      longitude)
    )
    self.db.commit()

  def user_exists(self, username, password):
    cursor = self.db.cursor()
    cursor.execute(
      "select id from users where username == ? and password == ?",
      (username, password))
    data = cursor.fetchone()
    print(data)
    return not (data == None)

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
    cursor.execute(
      "select username, latitude, longitude, id from users where username == ?",
      (username,)
    )
    data = cursor.fetchone()
    return {
      "username": data[0],
      "latitude": data[1],
      "longitude": data[2],
      "id": data[3]
    }