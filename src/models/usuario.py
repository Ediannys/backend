from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session
from src.models.profesor import Profesor
from passlib.hash import pbkdf2_sha256 as sha256
from flask import json
from flask import request

session = Session()

class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column(Integer, primary_key=True)
    idTipoUsuario = Column(Integer, ForeignKey('TipoUsuario.id'))
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    cedula = Column(String(20), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(250), nullable=False)

    pago_curso = relationship('PagoCurso')
    certificado = relationship('Certificado')
    profesor = relationship('Profesor', uselist=False, back_populates="usuario", cascade= "delete")
    estudiante = relationship('Estudiante', uselist=False, back_populates="usuario")
    prueba_estudiante = relationship('PruebaEstudiante')
    token_inscripcion = relationship("TokenInscripcion", uselist=False, back_populates="usuario")

    def __init__(self, idTipoUsuario, nombre, apellido, cedula, correo, contraseña):
        self.idTipoUsuario = idTipoUsuario
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.correo = correo
        self.contraseña = contraseña

    def __repr__(self):
        return '<Usuario: %r, %r>' % self.correo, self.contraseña

    @property
    def serialized(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cedula": self.cedula,
            "correo": self.correo,
            "tipo": self.idTipoUsuario
        }

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerUsuario(cls, id):
        return session.query(cls).get(id)

    @classmethod
    def obtenerEstudiante(cls, id):
        estudiante = session.query(cls).filter_by(id = id).first()
        return estudiante.serialized

    @classmethod
    def MostrarUsuarios(cls, id):
        users = session.query(Usuario).filter_by(idTipoUsuario=id).all()
        a_usuarios = []

        for i in range(0, len(users)):
            usuario = session.query(Usuario).filter_by(id=users[i].id)

            e = {
                "id": users[i].id,
                "nombre": users[i].nombre,
                "apellido": users[i].apellido,
                "cedula": users[i].cedula,
                "correo": users[i].correo,
                "tipo": users[i].idTipoUsuario
            }

            a_usuarios.append(e)

        return json.dumps(a_usuarios)

    @classmethod
    def EliminarUsuario(cls, id):
        user = session.query(Usuario).get(id)
        #profesor= session.query(Profesor).filter_by(idUsuario=user.id).first()
        #if profesor:
        #    return {'mensaje': 'El profesor {} no puede ser eliminado porque tiene un curso asociado'.format(user.nombre)}
        #else:
        e = {
                "id": user.id,
                "nombre": user.nombre,
                "apellido": user.apellido,
                "cedula": user.cedula,
                "correo": user.correo,
                "tipo": user.idTipoUsuario
            }
        session.delete(user)
        session.commit()
        return json.dumps(e)

    @classmethod
    def ModificarUsuario(cls, id):
        user = session.query(cls).get(id)
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        cedula = request.json['cedula']
        correo = request.json['correo']

        user.nombre = nombre
        user.apellido = apellido
        user.cedula = cedula
        user.correo = correo

        e = {
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "cedula": user.cedula,
            "correo": user.correo,
            "tipo": user.idTipoUsuario
        }
        
        session.commit()
        return json.dumps(e)

    @classmethod
    def GenerararHash(cls, contraseña):
        return sha256.hash(contraseña)

    @classmethod
    def VerificarHash(cls, contraseña, hash):
        return sha256.verify(contraseña, hash)

    @classmethod
    def BuscarCorreo(cls, correo):
        return session.query(cls).filter_by(correo=correo).first()