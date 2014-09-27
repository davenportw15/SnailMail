from flask import Flask, jsonify, session, request, redirect, url_for, render_template
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

# SQLite3 connection
db = sqlite3.connect(os.path.abspath("db.sqlite"), check_same_thread=False)

# Models
users = Users(db)
mail = Mail(db, users)

@app.route("/test")
def test():
  return "Test"

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
      print("{} {} {} {}".format(username, password, latitude, longitude))
      users.create_user(username, password, latitude, longitude)
      return "User {} created".format(username)
    else:
      flash("Complete all fields")
      return redirect(url_for("signup"))

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