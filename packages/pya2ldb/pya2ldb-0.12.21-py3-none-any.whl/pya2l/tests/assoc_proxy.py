
from sqlalchemy import and_
from sqlalchemy import Column, Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import join, ForeignKey
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import foreign, relation
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection

metadata = MetaData()
engine = create_engine("sqlite://", echo = True)
metadata.bind = engine

user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', String(255), unique=True),
    Column('password', String(255))
)

brand_table = Table(
    'brand', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255))
)

sales_rep_table = Table(
    'sales_rep', metadata,
    Column('brand_id', None, ForeignKey('brand.id'), primary_key=True),
    Column('user_id', None, ForeignKey('user.id'), primary_key=True),
    Column('commission_pct', Integer, default=0)
)


class User(object):
    def __init__(self, user_name=None, password=None):
        self.user_name=user_name
        self.password=password

class Brand(object):
    def __init__(self, name=None):
        self.name = name

#    users = association_proxy('sales_reps', 'user', creator=lambda u:SalesRep(user=u, commission_pct=10))
    commissions = association_proxy(
        "sales_reps_by_user",
        "commission_pct",
        creator = lambda key, value: SalesRep(user = key, commission_pct = value)
    )

class SalesRep(object):
    def __init__(self, user=None, brand=None, commission_pct=0):
        self.user = user
        self.brand = brand
        self.commission_pct=commission_pct


mapper(User, user_table, properties = dict(
    sales_rep = relation(SalesRep, backref = 'user', uselist = False))
)

reps_by_user_class = attribute_mapped_collection('user')

mapper(Brand, brand_table, properties = dict(
    sales_reps_by_user = relation(
        SalesRep,
        backref = 'brand',
        collection_class = reps_by_user_class)
    ,
    )
)

mapper(SalesRep, sales_rep_table)

metadata.create_all()

Session = sessionmaker(bind = engine)
engine.echo = True
session = Session()

b = Brand('Cool Clothing')
session.add(b)

u = User('rick', 'foo')
session.add(u)

metadata.bind.echo = True
session.flush()

print(b.users)
b.users.append(u)

print(b.users)

print(b.sales_reps_by_user)
session.flush()

