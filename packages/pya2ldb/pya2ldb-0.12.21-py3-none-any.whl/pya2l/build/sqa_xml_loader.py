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

from lxml import etree
import xml.etree.ElementTree as ET

Base = declarative_base()

dbname = r":memory:"

XML = r"F:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.cdfx"

try:
    os.unlink(dbname)
except Exception as e:
    pass

#doc = etree.ElementTree.parse(XML)
doc = etree.parse(XML)

engine = create_engine("sqlite:///{}".format(dbname), echo = True)

session = orm.Session(engine, autoflush = True, autocommit = False)

#doc = ElementTree.parse("test.xml")
#session.add(Document(file, doc))
#session.commit()

metadata = Base.metadata

Base.metadata.create_all(engine)

#u = Customer(name = "Mark", user_type = "customer", note_customer = 15,
#        address = Address(number = 221, street = "Bcker Street"))
#session.add(u)

session.flush()
session.commit()
