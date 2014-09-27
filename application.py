from flask import Flask
from sqlalchemy import *

app = Flask(__name__)

# SQLAlchemy configuration
db = create_engine("postgres://avgxpdgohdmvxj:WlP74JeHYwanbAoWs5kG0e1Jrz@ec2-54-225-135-30.compute-1.amazonaws.com:5432/d623bbr29bp99g")
metadata = BoundMetaData(db)


# Models
users = models.Users(metadata)
mail = models.Users(metadata)

@app.route("/api/mail"):
  pass

@app.route("/api/send"):
  pass

if __name__ == "__main__":
  app.run()