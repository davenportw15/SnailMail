from sqlalchemy import *

class Users:
  
  def __init__(self, metadata):
    self.metadata = metadata
    self.table = Table("users", self.metadata,
      Column("id", Integer, primary_key=True),
      Column("username", String),
      Column("password", String),
      Column("latitude", Numeric),
      Column("longitude", Numeric)
    )

  