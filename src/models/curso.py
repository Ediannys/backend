from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from flask import json
from flask import request
from flask import json, jsonify


session = Session()

class Curso(Base):
    __tablename__ = 'Curso'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(20), unique=True, nullable=False)
    descripcion = Column(String(200))
    fechaInicio = Column(Date, nullable=False)
    fechaFinal = Column(Date, nullable=False)
    precio = Column(Float, nullable=False)

    pago_curso = relationship('PagoCurso')
    certificado = relationship('Certificado')
    seccion = relationship('Seccion', cascade="delete")
    prueba = relationship("Prueba", uselist=False, back_populates="curso", cascade="delete")
    token_inscripcion = relationship("TokenInscripcion", uselist=False, back_populates="curso")

    def __init__(self, nombre, descripcion, fechaInicio, fechaFinal, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFinal = fechaFinal
        self.precio = precio

    def __repr__(self):
        return '<Curso: %r>' % self.nombre

    @property
    def serialized(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fechaInicio": self.fechaInicio,
            "fechaFinal": self.fechaFinal,
            "precio": self.precio
        }

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerCursos(cls):
        busqueda= session.query(cls).all()
        return busqueda

    @classmethod
    def BuscarId(cls, id):
        busqueda= session.query(cls).filter_by(id=id).first()
        return busqueda

    @classmethod
    def Buscar(cls, nombre):
        busqueda= session.query(cls).filter_by(nombre=nombre).first()
        return busqueda

    @classmethod
    def BuscarPorId(cls, id):
        busqueda= session.query(cls).filter_by(id=id).first()
        return busqueda

    @classmethod
    def MostrarCursos_2(cls):
        cursos = session.query(cls).all()
        a_cursos = []

        for i in range(0, len(cursos)):
            e = {
                "id": cursos[i].id,
                "nombre": cursos[i].nombre,
                "descripcion": cursos[i].descripcion,
                "fechaInicio": cursos[i].fechaInicio,
                "fechaFinal": cursos[i].fechaFinal,
                "precio": cursos[i].precio
            }
            a_cursos.append(e)

        return jsonify(a_cursos)


    @classmethod
    def MostrarCursos(cls):
        cursos = session.query(cls).all()
        a_cursos = []

        for i in range(0, len(cursos)):
            e = {
                "id": cursos[i].id,
                "nombre": cursos[i].nombre,
                "descripcion": cursos[i].descripcion,
                "inicia": cursos[i].fechaInicio.strftime("%d/%m/%y"),
                "finaliza": cursos[i].fechaFinal.strftime("%d/%m/%y"),
                "precio": cursos[i].precio
            }
            a_cursos.append(e)

        return json.dumps(a_cursos)

    @classmethod
    def EliminarCurso(cls, id):
        curso = session.query(cls).get(id)

        e = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "fechaInicio": curso.fechaInicio,
            "fechaFinal": curso.fechaFinal,
            "precio": curso.precio
        }

        session.delete(curso)
        session.commit()
        return json.dumps(e)


    @classmethod
    def ModificarCurso(cls, id):
        curso = session.query(cls).get(id)
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        fechaInicio = request.json['inicia']
        fechaFinal = request.json['finaliza']
        precio = request.json['precio']

        curso.nombre= nombre
        curso.descripcion= descripcion
        curso.fechaInicio= fechaInicio
        curso.fechaFinal= fechaFinal
        curso.precio=precio
        e = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "fechaInicio": curso.fechaInicio,
            "fechaFinal": curso.fechaFinal,
            "precio": curso.precio
        }
        session.commit()
        return json.dumps(e)