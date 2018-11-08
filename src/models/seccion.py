from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session

session = Session()

class Seccion(Base):
    __tablename__ = 'Seccion'

    id = Column(Integer, primary_key=True)
    idCurso = Column(Integer, ForeignKey('Curso.id'))
    nCupos = Column(Integer, nullable=False)
    cupos = Column(Integer, nullable=False)
    seccion = Column(String(2), nullable=False)

    estudiante = relationship('Estudiante', back_populates='seccion', cascade="delete")

    def __init__(self, idCurso, nCupos, cupos, seccion):
        self.idCurso = idCurso
        self.nCupos = nCupos
        self.cupos = cupos
        self.seccion = seccion

    def __repr__(self):
        return '<Seccion: %r>' % self.id

    @classmethod
    def obtenerSeccion(cls, id):
        return session.query(cls).get(id)

    @classmethod
    def obtenerSecciones(cls, idCurso):
        return session.query(cls).filter_by(idCurso=idCurso).all()

    @classmethod
    def obtenerSeccionCurso(cls, idCurso, id):
        return session.query(cls).filter_by(idCurso=idCurso, id=id).first()

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idCurso": self.idCurso,
            "nCupos": self.nCupos,
            "cupos": self.cupos,
            "seccion": self.seccion
        }

    def Crear(self):
        session.add(self)
        session.commit()