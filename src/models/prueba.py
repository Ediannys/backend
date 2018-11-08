from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from flask import json, jsonify

from src.models.curso import Curso
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.models.posible_respuesta import PosibleRespuesta

session = Session()

class Prueba(Base):
    __tablename__ = 'Prueba'

    id = Column(Integer, primary_key=True)
    idCurso = Column(Integer, ForeignKey('Curso.id'), unique=True)
    especialidad = Column(String(20))
    
    respuesta = relationship('Respuesta', cascade="delete")
    curso = relationship("Curso", uselist=False, back_populates="prueba")
    prueba_estudiante = relationship("PruebaEstudiante", uselist=False, back_populates="prueba", cascade="delete")

    def __init__(self, idCurso, especialidad):
        self.idCurso= idCurso
        self.especialidad = especialidad

    def __repr__(self):
        return '<Prueba: %r>' % self.id

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerCurso(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def obtenerPrueba(cls, idCurso):
        nombreCurso = Curso.BuscarId(idCurso)
        prueba = session.query(cls).filter_by(idCurso = idCurso).first()

        if prueba is None:
            return jsonify({"Mensaje": "No existe prueba aun para este curso"})

        preguntas = Pregunta.obtenerPregunta(prueba.id)
        respuestas = []
        examen = []

        for i in range(0, len(preguntas)):
            respuesta = Respuesta.obtenerRespuesta(preguntas[i].id)
            posibles_respuestas = PosibleRespuesta.obtenerPosiblesRespuestas(preguntas[i].id)

            respuestas = posibles_respuestas
            respuestas.append(respuesta[0])

            for j in range(0, len(respuesta)):
                print(respuesta[j].id)

            pregunta = {
                "idPrueba": prueba.id,
                "curso": nombreCurso.nombre,
                "pregunta": preguntas[i].pregunta,
                "idPregunta": preguntas[i].id,
                "ponderacion": preguntas[i].ponderacion,
                "respuestas": [{"id":r.id, "respuesta":r.respuesta} for r in respuestas]
            }
            examen.append(pregunta)

        return jsonify({"Examen": examen})

    @classmethod
    def calificar(cls, idCurso):

        prueba = session.query(cls).filter_by(idCurso = idCurso).first()
        preguntas = Pregunta.obtenerPregunta(prueba.id)
        respuestas = []

        for i in range(0, len(preguntas)):
            respuesta = Respuesta.obtenerRespuesta(preguntas[i].id)
            respuesta_calificada = {
                "idPregunta": preguntas[i].id,
                "idRespuesta": respuesta[0].id,
                "ponderacion": preguntas[i].ponderacion
            }
            respuestas.append(respuesta_calificada)

        return respuestas

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idCurso": self.idCurso,
            "especialidad": self.especialidad
        }

    @classmethod
    def BuscarCurso(cls, idCurso):
        curso = session.query(cls).filter_by(idCurso=idCurso).first()
        return curso

