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

class VersionAssociation(Base):

    __tablename__ = "version_association"

    discriminator = Column(types.String)
    __mapper_args__ = {"polymorphic_on": discriminator}

#    version = relationship("Version", backref="association")


class Version(Base):
    """
    """
    _association_id = Column(types.Integer, ForeignKey("version_association.rid"))
    association = relationship("VersionAssociation", backref="version", uselist = False)
    parent = association_proxy("association", "parent")
    versionIdentifier = StdString()


    __optional_elements__ = ( )

class HasVersions(object):

    @declared_attr
    def version_association_id(cls):
        return Column(types.Integer, ForeignKey("version_association.rid"))

    @declared_attr
    def version_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            "%sVersionAssociation" % name, (VersionAssociation,),
            dict(
                __tablename__ = None,
                __mapper_args__ = {"polymorphic_identity": discriminator},
            ),
        )

        cls.version = association_proxy(
            "version_association",
            "version",
            creator = lambda version: assoc_cls(version = version),
        )
        return relationship(
            assoc_cls, backref = backref("parent", uselist = False)
        )


class Header(Base, HasVersions):
    """
    """
    __tablename__ = "header"

    comment = StdString()

    project_no = relationship("ProjectNo", back_populates = "header", uselist = False)


class ProjectNo(Base):
    """
    """
    __tablename__ = "project_no"

    projectNumber = StdIdent()

    __optional_elements__ = ( )
    _header_rid = Column(types.Integer, ForeignKey("header.rid"))
    header = relationship("Header", back_populates = "project_no")


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

vv = Version(versionIdentifier = "This is Version 47.11")
session.add(vv)
l0 = []
l0.append(vv)

pjn = ProjectNo(projectNumber = "My Project#")
session.add(pjn)

hdr = Header(comment = "This is a header", project_no = pjn, version = l0)
session.add(hdr)

session.flush()
session.commit()
print("\n", vv)
print("\n", pjn)
print("\n", hdr)

