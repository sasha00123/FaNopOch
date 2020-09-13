from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from flask_login import UserMixin
from project.database import Base
from sqlalchemy.orm import relationship


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(120), unique=False)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


class Field(Base):
    __tablename__ = 'field'
    id = Column(Integer, primary_key=True)
    polygons = relationship("Polygon")


class Polygon(Base):
    __tablename__ = 'polygon'
    id = Column(Integer, primary_key=True)
    field = Column(Integer, ForeignKey('field.id'))
    bbox = Column(Text)
    point = Column(Text)


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    bbox = Column(Text)
    histogram = Column(Text)
    polygons = Column(Text)
    probability = Column(Float)
    solved = Column(Integer)

    def __init__(self, histogram=None, probability=None, solved=0, polygons=None):
        self.polygons = polygons
        self.histogram = histogram
        self.probability = probability
        self.solved = solved
