from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from src.models.curso import Curso
from src.models.seccion import Seccion

session = Session()

class Profesor(Base):
    __tablename__ = 'Profesor'

    id = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    idCurso = Column(ForeignKey('Curso.id'))
    idSeccion = Column(Integer, ForeignKey('Seccion.id'))

    usuario = relationship('Usuario', back_populates='profesor')
    curso = relationship('Curso')
    seccion = relationship('Seccion', cascade="delete")

    def __init__(self, idUsuario, idCurso, idSeccion):
        self.idUsuario = idUsuario
        self.idCurso = idCurso
        self.idSeccion = idSeccion

    def __repr__(self):
        return '<Profesor: %r>' % self.id

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idUsuario":self.idUsuario,
            "idCurso": self.idCurso,
            "idSeccion": self.idSeccion
        }

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerProfesor(cls, idUsuario):
        return session.query(cls).filter_by(idUsuario=idUsuario).all()

    @classmethod
    def BuscarNombre(cls, id):
        curso = session.query(Curso).get(id)
        return curso.nombre

    @classmethod
    def BuscarNombreYseccion(cls, nombre, seccion):
        curso = session.query(Curso).filter_by(nombre=nombre).first()
        seccion_curso = session.query(Seccion).filter_by(idCurso=curso.id, seccion=seccion).first()
        return seccion_curso