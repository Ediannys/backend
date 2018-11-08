from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class TokenInscripcion(Base):
    __tablename__ = 'TokenInscripcion'

    id = Column(Integer, primary_key=True)
    jti = Column(String(120))
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    idCurso = Column(Integer, ForeignKey('Curso.id'))
    
    usuario = relationship("Usuario", back_populates="token_inscripcion")
    curso = relationship("Curso", back_populates="token_inscripcion")