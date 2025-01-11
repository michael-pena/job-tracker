from base import Base
from sqlalchemy import create_engine, Column, Integer, String, Date

class Application(Base):
    __tablename__ = 'APPLICATIONS'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    company = Column(String)
    position = Column(String)
    date = Column(String)
    status = Column(String)
    offer = Column(String)
    accepted = Column(String)

    def __init__(self, company, position, date, status, offer, accepted):
        self.company = company
        self.position = position
        self.date = date
        self.status = status
        self.offer = offer
        self.accepted = accepted
    
    def __repr__(self):
        return f'Application({self.company}, {self.position}, {self.date}, {self.status}, {self.offer}, {self.accepted})'
        