#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.interfaces import PoolListener

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

"""
engine = create_engine(database_url)

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

from sqlalchemy import event
event.listen(engine, 'connect', _fk_pragma_on_connect)
"""

class ForeignKeysListener(PoolListener):
    def connect(self, dbapi_con, con_record):
        db_cursor = dbapi_con.execute('pragma foreign_keys=ON')
        print("FKs On???")

database_url = 'sqlite:///:memory:'

#engine = sa.create_engine(database_url, listeners=[ForeignKeysListener()], echo = True)

engine = create_engine("sqlite://", echo=True)
engine.execute('pragma foreign_keys=on')

Base = declarative_base()
metadata = Base.metadata

tab = sa.Table('sometable', metadata, sa.Column('id', sa.Integer, primary_key = True), sqlite_autoincrement = True)

print(tab)

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert a Person in the person table
new_person = Person(name='new person')
session.add(new_person)
#session.commit()
 
# Insert an Address in the address table
new_address = Address(post_code='00000', person=new_person)
session.add(new_address)
session.commit()

session.query(Person).all()
person = session.query(Person).first()
person.name
session.query(Address).filter(Address.person == person).all()
session.query(Address).filter(Address.person == person).one()
address = session.query(Address).filter(Address.person == person).one()
address.post_code

# gh_get.sh awesto django-shop &&  gh_get.sh mikebailey61 J1939_stack &&  gh_get.sh OSB-AG IsoAgLib