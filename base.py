# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///job_tracker.db', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()