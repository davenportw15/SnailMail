from flask import Flask, jsonify
import sqlite3
import os

from models.users import Users

app = Flask(__name__)

# SQLite3 connection
db = sqlite3.connect(os.path.abspath("db.sqlite"))

# Models
users = Users(db)

@app.route("/api/mail")
def api_mail():
  pass

@app.route("/api/send")
def api_send():
  pass

@app.route("/user/<id>")
def api_users(id):
  return jsonify(user=users.get_user(int(id)))

if __name__ == "__main__":
  app.run()