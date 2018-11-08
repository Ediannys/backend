from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, Session
from src.models.usuario import Usuario
from src.models.curso import Curso
from flask import json

session = Session()

class Estudiante(Base):
    __tablename__ = 'Estudiante'

    id = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    idCurso = Column(ForeignKey('Curso.id'))
    idSeccion = Column(Integer, ForeignKey('Seccion.id'))
    aprobado = Column(Boolean(), default=False)
    certificado = Column(Boolean(), default=False)

    usuario = relationship('Usuario', back_populates='estudiante')
    curso = relationship('Curso')
    asistencia = relationship('Asistencia')
    seccion= relationship('Seccion', back_populates='estudiante')

    def __init__(self, idUsuario, idCurso, idSeccion, aprobado):
        self.idUsuario = idUsuario
        self.idCurso = idCurso
        self.idSeccion = idSeccion
        self.aprobado = aprobado



    def __repr__(self):
        return '<Estudiante: %r>' % self.id

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerEstudiantes(cls, idSeccion):
        return session.query(cls).filter_by(idSeccion=idSeccion).all()

    @classmethod
    def Calificar(cls, idUsuario, aprobacion):
        estudiante = session.query(cls).filter_by(idUsuario=idUsuario).first()
        
        if aprobacion == 'True':
            estudiante.aprobado = True
            session.commit()
            
            return {
                "id": estudiante.id,
                "idUsuario": estudiante.idUsuario,
                "idCurso": estudiante.idCurso,
                "idSeccion": estudiante.idSeccion,
                "aprobado": estudiante.aprobado
            }

        if aprobacion == 'False':
            estudiante.aprobado = False
            session.commit()
            
            return {
                "id": estudiante.id,
                "idUsuario": estudiante.idUsuario,
                "idCurso": estudiante.idCurso,
                "idSeccion": estudiante.idSeccion,
                "aprobado": estudiante.aprobado
            }

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idUsuario": self.idUsuario,
            "idCurso": self.idCurso,
            "aprobado": self.aprobado,
            "certificado": self.certificado
        }

    @classmethod
    def AprobarEstudiante(cls, id):
        estudiante = session.query(cls).get(id)
        if estudiante.aprobado == False:
            estudiante.status = True
        else:
            estudiante.status = False
        session.commit()
        return estudiante.status

    @classmethod
    def CertificadoEstudiante(cls, id):
        estudiante = session.query(cls).get(id)
        if estudiante.aprobado == False:
            estudiante.status = True
        return estudiante.status

    @classmethod
    def MostrarEstAprobados(cls, idCurso):
        estudiantesDeCurso = session.query(cls).filter_by(idCurso=idCurso, aprobado=True).all()
        a_estudiantes = []
        for i in range(0, len(estudiantesDeCurso)):
            estudianteDeCurso = session.query(cls).filter_by(id=estudiantesDeCurso[i].id).first()
            usuario = session.query(Usuario).filter_by(id=estudiantesDeCurso[i].idUsuario).first()
            curso = session.query(Curso).filter_by(id=estudiantesDeCurso[i].idCurso).first()
            e = {
                "id": estudianteDeCurso.id,
                "cedula": usuario.cedula,
                "apellido": usuario.apellido,
                "nombre": usuario.nombre,
                "curso": curso.nombre,
                "correo": usuario.correo,
                "status": estudianteDeCurso.aprobado,
                "certificado": estudianteDeCurso.certificado
            }
            a_estudiantes.append(e)
        return json.dumps(a_estudiantes)

    @classmethod
    def AprobarEnvio(cls, id):
        estudiante = session.query(cls).get(id)
        if estudiante.certificado == False:
            estudiante.certificado = True
