import os
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("postgresql://postgres:1111@localhost:5432/booking")

Session = sessionmaker(bind=engine)
BaseModel = declarative_base()


class Users(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    user_status = Column(Integer)


class Rooms(BaseModel):
    __tablename__ = "rooms"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    name = Column(String)
    num_of_seats = Column(Integer)


class booked_room(BaseModel):
    __tablename__ = "booked_room"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    num_of_people = Column(Integer)
    time_start = Column(TIMESTAMP)
    time_end = Column(TIMESTAMP)
    userToBook = relationship(Users, foreign_keys=[user_id], backref="user_id", lazy="joined")
    roomToBook = relationship(Rooms, foreign_keys=[room_id], backref="room_id", lazy="joined")