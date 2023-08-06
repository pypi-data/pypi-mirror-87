
from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import join
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import foreign
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<User(%s)>" % self.name

class Team(Base):

    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Team(%s)>" % self.name

class Role(Base):
    __tablename__ = "role"

    id =Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(%s)>" % self.name

e = create_engine("sqlite://", echo=True)


s = Session(e)
Base.metadata.create_all(e)
