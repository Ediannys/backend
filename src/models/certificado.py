from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from .base import Base, Session

session = Session()

class Certificado(Base):
    __tablename__ = 'Certificado'

    id = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    idCurso = Column(Integer, ForeignKey('Curso.id'))
    entregado = Column(Boolean(), default=False)

    def __init__(self, idUsuario, idCurso, entregado):
        self.idUsuario = idUsuario,
        self.idCurso= idCurso,
        self.entregado= entregado

    def __repr__(self):
        return '<Certificado: %r>' % self.id

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idUsuario": self.idUsuario,
            "idCurso": self.idCurso,
            "entregado": self.entregado

        }