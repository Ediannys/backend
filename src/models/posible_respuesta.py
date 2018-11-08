from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from flask import json
from flask import request

session = Session()

class PosibleRespuesta(Base):
    __tablename__ = 'PosibleRespuesta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    idPregunta = Column(Integer, ForeignKey('Pregunta.id'))
    respuesta = Column(String(200))

    def __init__(self, idPregunta, respuesta):
        self.idPregunta= idPregunta
        self.respuesta = respuesta

    def __repr__(self):
        return '<Respuesta: %r>' % self.respuesta

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerPosiblesRespuestas(cls, idPregunta):
        return session.query(cls).filter_by(idPregunta = idPregunta).all()

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idPregunta": self.idPregunta,
            "respuesta": self.respuesta
        }

    @classmethod
    def EliminarPosibleRespuesta(cls, id):
        pos_respuesta = session.query(cls).get(id)
        e = {
            "id": pos_respuesta.id,
            "idPregunta": pos_respuesta.idPregunta,
            "respuesta": pos_respuesta.respuesta
        }
        session.delete(pos_respuesta)
        session.commit()
        return json.dumps(e)

    @classmethod
    def ModificarPosibleRespuesta(cls, id):
        consulta = session.query(cls).get(id)
        posible_respuesta = request.json['respuesta']
        consulta.respuesta = posible_respuesta
        e = {
            "id": consulta.id,
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
                "idPregunta": respuestas[i].idPregunta,
                "respuesta": respuestas[i].respuesta
            }
            a_respuestas.append(e)
        return json.dumps(a_respuestas)