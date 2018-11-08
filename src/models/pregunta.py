from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from flask import json, jsonify
from flask import request
from src.models import prueba

session = Session()

class Pregunta(Base):
    __tablename__ = 'Pregunta'

    id = Column(Integer, primary_key=True)
    idPrueba = Column(Integer, ForeignKey('Prueba.id'))
    pregunta = Column(String(200), nullable=False)
    ponderacion = Column(Integer, nullable=False)

    respuesta = relationship("Respuesta", uselist=False, back_populates="pregunta")
    posible_respuesta = relationship("PosibleRespuesta")

    def __init__(self, idPrueba, pregunta, ponderacion):
        self.idPrueba= idPrueba
        self.pregunta = pregunta
        self.ponderacion = ponderacion

    def __repr__(self):
        return '<Pregunta: %r>' % self.pregunta

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerPregunta(cls, idPrueba):
        return session.query(cls).filter_by(idPrueba = idPrueba).all()

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idPrueba": self.idPrueba,
            "pregunta": self.pregunta,
            "ponderacion": self.ponderacion
        }

    @classmethod
    def EliminarPregunta(cls, id):
        pregunta = session.query(cls).get(id)
        e = {
            "id": pregunta.id,
            "idPrueba": pregunta.idPrueba,
            "pregunta": pregunta.pregunta,
            "ponderacion": pregunta.ponderacion,

        }
        session.delete(pregunta)
        session.commit()
        return json.dumps(e)

    @classmethod
    def ModificarPregunta(cls, id):
        consulta = session.query(cls).get(id)
        pregunta = request.json['pregunta']
        ponderacion = request.json['ponderacion']

        consulta.pregunta = pregunta
        consulta.ponderacion = ponderacion
        e = {
            "id": consulta.id,
            "idPrueba": consulta.idPrueba,
            "pregunta": consulta.pregunta,
            "ponderacion": consulta.ponderacion
        }
        session.commit()
        return json.dumps(e)

    @classmethod
    def MostrarPreguntas(cls, id):
        test = session.query(prueba.Prueba).filter_by(idCurso=id).first()
        preguntas = session.query(cls).filter_by(idPrueba=test.id).all()
        a_preguntas = []
        for i in range(0, len(preguntas)):
            e = {
                "id": preguntas[i].id,
                "idPrueba": preguntas[i].idPrueba,
                "pregunta": preguntas[i].pregunta,
                "ponderacion": preguntas[i].ponderacion,   
            }
            a_preguntas.append(e)
        return json.dumps(a_preguntas)

    @classmethod
    def MostrarPregunta(cls, id):
        pregunta = session.query(cls).get(id)
        e = {
            "id": pregunta.id,
            "idPrueba": pregunta.idPrueba,
            "pregunta": pregunta.pregunta,
            "ponderacion": pregunta.ponderacion,
        }
        return json.dumps(e)