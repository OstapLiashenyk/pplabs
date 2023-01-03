from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from models import *

engine = create_engine("postgresql://postgres:1111@localhost:5432/booking", echo=True)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()