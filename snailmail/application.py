from flask import Flask, jsonify, session, request, redirect, url_for, render_template, flash, g
import sqlite3
import os
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
print(sys.path)

from snailmail.models.user import User
from snailmail.models.mail import Mail
from snailmail.database import db_session



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
# db = sqlite3.connect(os.path.abspath("db.sqlite"), check_same_thread=False)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/whoami")
def test():
    top = session.get('user')
    toret = repr(User.unserialize(top,db_session))
    print(toret)
    return toret.replace("<","&lt;").replace(">","&gt;")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "GET":
    return render_template("signup.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    try:
      if not (username and password and longitude and latitude):
          raise Exception("Complete all fields")
      print(username)
      print(password)
      print(longitude)
      print(latitude)
      user =\
              User(
                    username, 
                    password, 
                    latitude, 
                    longitude
                    )
      db_session.add(user)
      db_session.commit()
      session['user'] = user.serialize()
      return redirect(url_for("dashboard"))
    except Exception as err:
      flash(str(err))
      import traceback
      print(traceback.format_exc())
      return redirect(url_for("signup"))

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        try:
            session['user'] = User.get_user(username,password,db_session).\
                    serialize()
            return redirect(url_for("dashboard"))
        except Exception as ext:
            flash(str(ext))
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
  if "user" in session:
      print("session user: ", session.get("user"))
      mails = db_session.query(Mail).join(User,User.id==Mail.recipient_id).all()
      if mails is not None:
        tojson = [mail.serialize() for mail in mails]
      return jsonify(mail=tojson)
  else:
    return jsonify(mail=[])

@app.route("/api/send", methods=["POST"])
def api_send():
    sent_mail = request.json
    print(request.json)
    print(session['user'])
    now = datetime.now()
    if "content" in sent_mail and\
            "user" in session and\
            "recipient_username" in sent_mail and\
            "subject" in sent_mail:
        try:
            recipient = User.get_user_by_username(
                    sent_mail['recipient_username'],db_session)
            if recipient is None:
                raise Exception('User ' + sent_mail['recipient_username']
                        + ' not found!')
            recipient_id = recipient.id
            tosend = Mail(sent_mail['subject'],
                    sent_mail['content'],
                    now,
                    (session['user'])['id'],
                    recipient_id
                    )
            tosend.set_delay()
            db_session.add(tosend)
            db_session.commit()
            return jsonify(status=True)
        except Exception as err:
            flash(str(err))
            import traceback
            print(traceback.format_exc())
            return jsonify(status=False,errmsg=err.args[0])
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

