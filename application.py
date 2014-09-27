from flask import Flask, jsonify, session, request, redirect, url_for, render_template, flash
import sqlite3
import os

from models.users import Users
from models.mail import Mail

class FlaskAngular(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
))


app = FlaskAngular(__name__)
app.config['DEBUG'] = True
app.secret_key = "2jfj9pj9f$$$kldjflkj2kljfkj###23jlkjl@"

# SQLite3 connection
db = sqlite3.connect(os.path.abspath("db.sqlite"), check_same_thread=False)

# Models
users = Users(db)
mail = Mail(db, users)

@app.route("/whoami")
def test():
  return session.get("username")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "GET":
    return render_template("signup.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    if username and password and longitude and latitude:
      users.create_user(username, password, latitude, longitude)
      session["username"] = username
      return redirect(url_for("dashboard"))
    else:
      flash("Complete all fields")
      return redirect(url_for("signup"))

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
      if users.user_exists(username, password):
        session["username"] = username
        return redirect("dashboard")
      else:
        flash("Username and password do not match an account")
        return redirect(url_for("login"))
    else:
      flash("Complete all fields")
      return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET"])
def dashboard():
  return render_template("mail.html")

# API
@app.route("/api/mail")
def api_mail():
  if "username" in session:
    return jsonify(mail=mail.get_mail_for_user(session.get("username")))
  else:
    return jsonify(mail=[])

@app.route("/api/send", methods=["POST"])
def api_send():
  sent_mail = request.json
  if "content" in sent_mail and "date_sent" in sent_mail and "sender" in sent_mail and "recipient" in sent_mail and "subject" in sent_mail:
    mail.create_mail(sent_mail["content"], sent_mail["date_sent"], sent_mail["sender"], sent_mail["recipient"], sent_mail["subject"])
    return jsonify(status=True)
  else:
    return jsonify(status=False)

@app.route("/user/<id>")
def api_users(id):
  return jsonify(user=users.get_user(id))

@app.route("/mail/<user>")
def api_mail_for_user(user):
   return jsonify(mail=mail.get_mail_for_user(user))

if __name__ == "__main__":
  app.run()