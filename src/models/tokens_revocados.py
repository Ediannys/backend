from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import Base, Session

session = Session()

class TokensRevocados(Base):
    __tablename__ = 'TokensRevocados'
    
    id = Column(Integer, primary_key=True)
    jti = Column(String(120))
    
    def add(self):
        session.add(self)
        session.commit()