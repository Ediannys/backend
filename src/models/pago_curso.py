from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, Session
from src.models.usuario import Usuario
from src.models.curso import Curso
from flask import json

session = Session()

class PagoCurso(Base):
    __tablename__ = 'PagoCurso'

    id = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    idCurso = Column(Integer, ForeignKey('Curso.id'))
    nTransferencia = Column(String(25), unique=True, nullable=False)
    monto = Column(Float, nullable=False)
    fechaPago = Column(Date, nullable=False)
    status = Column(Boolean(), default=False)
    
    def __init__(self, idUsuario, idCurso, nTransferencia, monto, fechaPago):
        self.idUsuario = idUsuario,
        self.idCurso=idCurso,
        self.nTransferencia = nTransferencia,
        self.monto = monto,
        self.fechaPago= fechaPago

    def __repr__(self):
        return '<Pago: %r>' % self.id

    @property
    def serialized(self):
        return {
            "id": self.id,
            "idUsuario": self.idUsuario,
            "idCurso": self.idCurso,
            "monto": self.monto,
            "nTransferencia": self.nTransferencia,
            "monto": self.monto,
            "fechaPago": self.fechaPago,
            "status": self.status
        }

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def cursosPagadosPorUsuario(cls, idUsuario):
        return session.query(cls).filter_by(idUsuario=idUsuario).all()

    @classmethod
    def AprobarTransferencia(cls, id):
        pago_c = session.query(cls).get(id)

        if pago_c.status == False:
            pago_c.status= True   
        else:
            pago_c.status= False

        session.commit()
        return pago_c.status

    @classmethod
    def MostrarPagos(cls, idCurso):
        pagos_cursos = session.query(cls).filter_by(idCurso=idCurso).all()
        a_pagos=[]

        for i in range(0, len(pagos_cursos)):
            pago_c= session.query(cls).filter_by(id=pagos_cursos[i].id).first()
            usuario= session.query(Usuario).filter_by(id=pagos_cursos[i].idUsuario).first()
            curso= session.query(Curso).filter_by(id=pagos_cursos[i].idCurso).first()

            e = {
                "id": pago_c.id,
                "cedula": usuario.cedula,
                "apellido": usuario.apellido,
                "nombre": usuario.nombre,
                "curso": curso.nombre,
                "transferencia": pago_c.nTransferencia,
                "fecha": pago_c.fechaPago,
                "monto": pago_c.monto,
                "status": pago_c.status
            }

            a_pagos.append(e)
            
        return json.dumps(a_pagos)

    @classmethod
    def verificarTransferencia(cls, nTransferencia):
        return session.query(cls).filter_by(nTransferencia=nTransferencia).first()

