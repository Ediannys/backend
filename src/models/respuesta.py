from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from flask import json
from flask import request

session = Session()

class Respuesta(Base):
    __tablename__ = 'Respuesta'

    id = Column(Integer, primary_key=True)
    idPrueba = Column(Integer, ForeignKey('Prueba.id'))
    idPregunta = Column(Integer, ForeignKey('Pregunta.id'))
    respuesta = Column(String(200))

    pregunta = relationship("Pregunta", back_populates="respuesta")

    def __init__(self, idPrueba, idPregunta, respuesta):
        self.idPrueba= idPrueba
        self.idPregunta= idPregunta
        self.respuesta = respuesta

    def __repr__(self):
        return '<Respuesta: %r>' % self.respuesta

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerRespuesta(cls, idPregunta):
        return session.query(cls).filter_by(idPregunta = idPregunta).all()

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idPrueba": self.idPrueba,
            "idPregunta": self.idPregunta,
            "respuesta": self.respuesta
        }

    @classmethod
    def EliminarRespuesta(cls, id):
        respuesta = session.query(cls).get(id)
        e = {
            "id": respuesta.id,
            "idPrueba": respuesta.idPrueba,
            "idPregunta": respuesta.idPregunta,
            "respuesta": respuesta.respuesta,

        }
        session.delete(respuesta)
        session.commit()
        return json.dumps(e)

    @classmethod
    def ModificarRespuesta(cls, id):
        consulta = session.query(cls).get(id)
        respuesta = request.json['respuesta']
        consulta.respuesta = respuesta
        e = {
            "id": consulta.id,
            "idPrueba": consulta.idPrueba,
            "idPregunta": consulta.idPregunta,
            "respuesta": consulta.respuesta
        }
        session.commit()
        return json.dumps(e)

    @classmethod
    def MostrarRespuestas(cls, id):

        respuestas = session.query(cls).filter_by(idPregunta=id).all()
        a_respuestas = []
        for i in range(0, len(respuestas)):
            e = {
                "id": respuestas[i].id,
                "idPrueba": respuestas[i].idPrueba,
                "idPregunta": respuestas[i].idPregunta,
                "respuesta": respuestas[i].respuesta,
            }
            a_respuestas.append(e)
        return json.dumps(a_respuestas)