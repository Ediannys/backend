from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session

session = Session()

class Asistencia(Base):
    __tablename__ = 'Asistencia'

    id = Column(Integer, primary_key=True)
    idEstudiante = Column(Integer, ForeignKey('Estudiante.id'))
    fecha = Column(Date)

    def __init__(self, idEstudiante, fecha):
        self.idEstudiante= idEstudiante
        self.fecha = fecha

    def __repr__(self):
        return '<Asistencia: %r, Fecha: %r>' % self.id, self.fecha

    def Crear(self):
        session.add(self)
        session.commit()

    @property
    def serialized(self):
        return {
            "id": self.id,
            "fecha": self.fecha
        }