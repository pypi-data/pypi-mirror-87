
from functools import partial
import mmap
import os
import re
import sqlite3

from sqlalchemy import (MetaData, schema, types, orm, event,
            create_engine, Column, ForeignKey, ForeignKeyConstraint, func,
                PassiveDefault, UniqueConstraint, CheckConstraint
                )
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine
from sqlalchemy.sql import exists

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(types.Integer, primary_key = True)
    name = Column(types.String(50), unique = False)
    user_type = Column(types.String(32), nullable = False)

    address = relationship("Address", uselist = False, back_populates = "user")

    __mapper_args__ = {
        "polymorphic_on": "user_type",
        "polymorphic_identity": "user_type"
    }

class Customer(User):
    __tablename__ = "customer"
    id = Column(types.Integer, ForeignKey("user.id"), primary_key = True)
    note_customer = Column(types.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "customer"
    }


class Provider(User):
    __tablename__ = "provider"
    id = Column(types.Integer, ForeignKey("user.id"), primary_key = True)
    note_provider = Column(types.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "provider"
    }


class Address(Base):
    __tablename__ = "address"
    id = Column(types.Integer, primary_key = True)
    number = Column(types.Integer)
    street = Column(types.String(100))
    user_id = Column(types.Integer, ForeignKey("user.id"))
    #user = relationship(User, backref = backref("address", uselist = False))
    user = relationship(User, back_populates = "address")

#dbname = ":memory:"
dbname = "poly.sqlite"


try:
    os.unlink(dbname)
except Exception as e:
    pass

engine = create_engine("sqlite:///{}".format(dbname), echo = True)

session = orm.Session(engine, autoflush = True, autocommit = False)

metadata = Base.metadata

Base.metadata.create_all(engine)

u = Customer(name = "Mark", user_type = "customer", note_customer = 15,
        address = Address(number = 221, street = "Bcker Street"))
session.add(u)

session.flush()
session.commit()

#print(dir(Provider.note_provider))
