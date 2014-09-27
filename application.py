from flask import Flask, jsonify, session, request, redirect, url_for
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

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "GET":
    render_template() #RENDER SOME TEMPLATE
  else: # If form posted
    username = request.form.get("username")
    password = request.form.get("password")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    if username && password && latitude && longitude:
      users.create_user(username, password, latitude, longitude)
    else:
      flash("Complete all fields")
      redirect(url_for("signup"))


# API

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