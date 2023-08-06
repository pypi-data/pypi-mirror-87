from functools import partial
import mmap
import re
import sqlite3

from sqlalchemy import (MetaData, schema, types, orm, event,
    create_engine, Column, ForeignKey, ForeignKeyConstraint, func,
    PassiveDefault, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine
from sqlalchemy.sql import exists

@as_declarative()
class Base(object):

    rid = Column("rid", types.Integer, primary_key = True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        columns = [c.name for c in self.__class__.__table__.c]
        result = []
        for name, value in [(n, getattr(self, n)) for n in columns if not n.startswith("_")]:
            if isinstance(value, str):
                result.append("{} = '{}'".format(name, value))
            else:
                result.append("{} = {}".format(name, value))
        return "{}({})".format(self.__class__.__name__, ", ".join(result))

def StdFloat(default = 0.0):
    return Column(types.Float, default = default, nullable = False)

def StdShort(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (-32768, 32767)')
    )

def StdUShort(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (0, 65535)')
    )

def StdLong(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (-2147483648, 2147483647)')
    )

def StdULong(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (0, 4294967295)')
    )

def StdString(default = 0, primary_key = False, unique = False):
    return Column(types.VARCHAR(256), default = default, nullable = False,
        primary_key = primary_key, unique = unique,
    )

def StdIdent(default = 0, primary_key = False, unique = False):
    return Column(types.VARCHAR(1025), default = default, nullable = False,
        primary_key = primary_key, unique = unique,
    )


class CompuTabPair(Base):

    __tablename__ = "compu_tab_pair"

    ct_rid = Column(types.Integer, ForeignKey("compu_tab.rid"))

    inVal = StdFloat()
    outVal = StdFloat()


class CompuTab(Base):

    __tablename__ = "compu_tab"

    name = StdIdent()
    longIdentifier = StdString()
    conversionType = StdString()
    numberValuePairs = StdUShort()

    pairs = relationship("CompuTabPair", backref = "parent", cascade="all, delete-orphan", passive_deletes = True)

class CalHandles(Base):

    __tablename__ = "calhandles"

    ch_rid = Column(types.Integer, ForeignKey("calibration_handle.rid"))
    handle = StdLong()

    def __init__(self, handle):
        self.handle = handle


class CalibrationHandle(Base):

    __tablename__ = "calibration_handle"

    _handles = relationship("CalHandles", backref = "parent")
    handles = association_proxy("_handles", "handle")

##
##
##
engine = create_engine("sqlite:///:memory:", echo = True,
            connect_args={'detect_types': sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES},
        native_datetime = True)

session = orm.Session(engine, autoflush = False, autocommit = False)
metadata = Base.metadata
Base.metadata.create_all(engine)
session.flush()
session.commit()


ch = CalibrationHandle(handles = [1,2,3,5,8,13])
p0 = CompuTabPair(inVal = 1, outVal = 1.34)
p1 = CompuTabPair(inVal = 2, outVal = 5.6)
session.add(p0)
session.add(p1)
ct = CompuTab(name = "CT#1", longIdentifier = "This is a computab", conversionType = "TAB_INTERP", numberValuePairs = 3)
session.add(ct)
ct.pairs.append(p0)
ct.pairs.append(p1)
session.commit()
print("\n")
print(ct)
print(ct.pairs)
print(ch.handles)
