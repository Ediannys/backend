from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import Base, Session

session = Session()

class TipoUsuario(Base):
    __tablename__ = 'TipoUsuario'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(15), unique=True , nullable=False)
    
    usuario = relationship("Usuario")

    def __init__(self, tipo):
        self.tipo = tipo

    def __repr__(self):
        return '<Usuario: %r>' % self.tipo

    @property
    def serialized(self):
        return {
            "id": self.id,
            "tipo": self.tipo
        }