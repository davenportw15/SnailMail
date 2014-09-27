class Users:

  def __init__(self, db):
    self.db = db

  def create_user(self, username, password, longitude, latitude):
    cursor = self.db.cursor()
    cursor.execute(
      "insert into users (username, password, longitude, latitude) values (?, ?, ?, ?)",
      (username,
      password,
      longitude,
      latitude)
    )
    self.db.commit()

  def get_user(self, id):
    cursor = self.db.cursor()
    cursor.execute(
      "select username, latitude, longitude from users where id == ?",
      (id,)
    )
    data = cursor.fetchone()
    return {
      "username": data[0],
      "latitude": data[1],
      "longitude": data[2]
    }