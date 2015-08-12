#!/usr/bin/env python3

#file to manage sqlalchemy orm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

conn_string = os.path.join(os.path.dirname(__file__), 'db.sqlite')

engine = create_engine('sqlite:///' + conn_string,
        convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import snailmail.models.mail
    import snailmail.models.user
    Base.metadata.create_all(bind=engine)

