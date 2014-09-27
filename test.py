import sqlite3
import os

from models.users import Users
from models.mail import Mail

# SQLite3 connection
db = sqlite3.connect(os.path.abspath("db.sqlite"))

# Models
users = Users(db)
mail = Mail(db, users)

#users.create_user("Greg", "test123123", 49, 2)
users.create_user("Will", "testset", 42, -71)
users.create_user("Pegram", "testset3123", 42, -71)

# Create mail
#mail.create_mail(
#  "Mail with delay",
#  "2014-09-27",
#  "Will",
#  "Greg",
#  "Here's a subject."
#)

mail.create_mail(
  "Mail with delay for Dr. Pegram",
  "2014-09-27",
  "Will",
  "Pegram",
  "NOSB NOSB NOSB"
)



mail.get_mail_for_user("Pegram")