from flask import jsonify

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session

from src.models.prueba import Prueba
from src.models.pago_curso import PagoCurso
from src.models.curso import Curso
from src.models.seccion import Seccion

session = Session()

class PruebaEstudiante(Base):
    __tablename__ = 'PruebaEstudiante'

    id = Column(Integer, primary_key=True)
    idPrueba = Column(Integer, ForeignKey('Prueba.id'))
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    calificacion = Column(Integer, nullable=False)

    prueba = relationship('Prueba', back_populates='prueba_estudiante')

    def __init__(self, idUsuario, idPrueba, calificacion):
        self.idUsuario = idUsuario
        self.idPrueba = idPrueba
        self.calificacion = calificacion

    def __repr__(self):
        return '<PruebaEstudiante: %r>' % self.id

    def Crear(self):
        session.add(self)
        session.commit()

    @classmethod
    def obtenerIdPrueba(cls, idUsuario):
        return session.query(cls).filter_by(idUsuario=idUsuario).all()

    @classmethod
    def obtenerCursosPreInscritos(cls, idUsuario):
        idCursosPreInscritos = []
        cursosPreInscritos = []
        cursosPagados = PagoCurso.cursosPagadosPorUsuario(idUsuario)
        pruebas = cls.obtenerIdPrueba(idUsuario)
        cursos = []
        cont = 0

        if pruebas == []:
            return {"mensaje": "Este usuario no tiene examenes aprobados"}

        for i in range(0, len(pruebas)):
            idCursosPreInscritos.append(Prueba.obtenerCurso(pruebas[i].idPrueba))

        if not cursosPagados:
            for i in range(0, len(idCursosPreInscritos)):
                cursosPreInscritos.append(Curso.BuscarId(idCursosPreInscritos[i].idCurso))

            for i in range(0, len(cursosPreInscritos)):
                secciones = Seccion.obtenerSecciones(cursosPreInscritos[i].id)
                seccions = [seccion.serialized for seccion in secciones]
                curso = {
                    "id": cursosPreInscritos[i].id,
                    "nombre": cursosPreInscritos[i].nombre,
                    "descripcion": cursosPreInscritos[i].descripcion,
                    "fechaInicio": cursosPreInscritos[i].fechaInicio,
                    "fechaFinal": cursosPreInscritos[i].fechaFinal,
                    "precio": cursosPreInscritos[i].precio,
                    "secciones": seccions
                }
                cursos.append(curso)
            return jsonify({"Cursos": cursos})

        for i in range(0, len(idCursosPreInscritos)):
            
            cursosPreInscritos.append(Curso.BuscarId(idCursosPreInscritos[i].idCurso))
            secciones = Seccion.obtenerSecciones(cursosPreInscritos[i].id)
            cont = 0
            for j in range(0, len(cursosPagados)):
                if cursosPreInscritos[i].id == cursosPagados[j].idCurso:
                    cont = cont + 1
                    print('hola')

            if cont == 0:
                seccions = [seccion.serialized for seccion in secciones]
                curso_2 = {
                        "id": cursosPreInscritos[i].id,
                        "nombre": cursosPreInscritos[i].nombre,
                        "descripcion": cursosPreInscritos[i].descripcion,
                        "fechaInicio": cursosPreInscritos[i].fechaInicio,
                        "fechaFinal": cursosPreInscritos[i].fechaFinal,
                        "precio": cursosPreInscritos[i].precio,
                        "secciones": seccions
                    }
                cursos.append(curso_2)

        return jsonify({"Cursos": cursos})

    @classmethod
    def existe(cls, idUsuario, idPrueba):
        existe = session.query(cls).filter_by(idUsuario=idUsuario, idPrueba=idPrueba).first()
        return existe

    @property
    def serialized(self):
        return {
            "id": self.id,
            "calificacion": self.calificacion
        }