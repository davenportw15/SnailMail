from flask import Flask, jsonify
import sqlite3
import os

from models.users import Users
from models.mail import Mail

app = Flask(__name__)

# SQLite3 connection
db = sqlite3.connect(os.path.abspath("db.sqlite"))

# Models
users = Users(db)
mail = Mail(db)

@app.route("/api/mail")
def api_mail():
  pass

@app.route("/api/send")
def api_send():
  pass

@app.route("/user/<id>")
def api_users(id):
  return jsonify(user=users.get_user(id))

@app.route("/mail/<user>")
def api_mail_for_user(user):
   return jsonify(mail=mail.get_mail_for_user(user))

if __name__ == "__main__":
  app.run()