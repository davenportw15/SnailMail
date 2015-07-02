from models import secure_pass

class Users:

  def __init__(self, db):
    self.db = db

  def create_user(self, username, password, latitude, longitude):
    sp = secure_pass.Password(password)
    password_key = sp.get_hash()
    password_salt = sp.get_salt()
    cursor = self.db.cursor()
    cursor.execute(
      "insert into users (username, password_key, password_salt, latitude, longitude) values (?, ?, ?, ?, ?)",
      (username,
      password_key,
      password_salt,
      latitude,
      longitude)
    )

    self.db.commit()

  def user_exists(self, username, password):
    cursor = self.db.cursor()
    # get the salt, key for the username
    cursor.execute("select password_salt, password_key from users where username == ?",
            (username,))
    row = cursor.fetchone()
    if row is None:
        return False

    salt = row[0]
    key = row[1]

    return secure_pass.Password.check_pass(
            password,
            key,
            salt
            )


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
