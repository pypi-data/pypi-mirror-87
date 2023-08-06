
from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import join, ForeignKey
from sqlalchemy import String, UniqueConstraint
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

class Membership(Base):
    __tablename__ = "membership"

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)

    UniqueConstraint('user_id', 'team_id', 'role_id')
    user = relationship('User', uselist=False, backref='memberships')
    team = relationship('Team', uselist=False, backref='memberships')
    role = relationship('Role', uselist=False, backref='memberships')

    def __init__(self, user, team, role):
        self.user_id = user.id
        self.team_id = team.id
        self.role_id = role.id

    def __repr__(self):
        return "<Membership({} {} {})>".format(self.user, self.team, self.role)


e = create_engine("sqlite://", echo=True)


s = Session(e)
Base.metadata.create_all(e)

u = User("Chris")
t = Team("Hartt-Schwanz")
r = Role("Führer")
s.add_all([u, t, r])
s.flush()
s.flush()
m = Membership(u, t, r)
s.add(m)
s.commit()
u2 = s.query(User).get(1)
print(u2.memberships)
