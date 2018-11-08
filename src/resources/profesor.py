import datetime
from datetime import date
from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.profesor import Profesor
from src.models.seccion import Seccion
from src.models.curso import Curso
from src.models.estudiante import Estudiante
from src.models.usuario import Usuario
from src.models.asistencia import Asistencia

class CursoSeccion(Resource):
    
    def get(self, idProfesor):
        profesor = Profesor.obtenerProfesor(idProfesor)
        cursos_secciones = []

        for i in range(0, len(profesor)):
            curso = Curso.BuscarId(profesor[i].idCurso)
            seccion = Seccion.obtenerSeccion(profesor[i].idSeccion)
            curso_seccion = {
                "idCurso": curso.id,
                "Curso": curso.nombre,
                "idSeccion": seccion.id,
                "Seccion": seccion.seccion,
            }
            cursos_secciones.append(curso_seccion)

        
        return jsonify(cursos_secciones)

class EstudianteSeccion(Resource):

    def get(self, idSeccion):

        estudiantes_seccion = Estudiante.obtenerEstudiantes(idSeccion)
        estudiantes = []

        for i in range(0, len(estudiantes_seccion)):
            student = Usuario.obtenerUsuario(estudiantes_seccion[i].idUsuario)
            estudiante = {
                "id": student.id,
                "nombre": student.nombre,
                "apellido": student.apellido,
                "cedula": student.cedula,
                "correo": student.correo,
                "tipo": student.idTipoUsuario
            }
            estudiantes.append(estudiante)
        
        return jsonify(estudiantes)

class CalificarEstudiante(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', help='Este campo es requerido', required=True)
    parser.add_argument('aprobacion', help='Este campo es requerido', required=True)

    def post(self):
        data = self.parser.parse_args()
        resultado = Estudiante.Calificar(data['id'], data['aprobacion'])
        return jsonify(resultado)


class RegistrarAsistencia(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('idEstudiante', help='Este campo es requerido', required=True)
    parser.add_argument('fecha', help='Este campo es requerido', required=True)

    def post(self):
        data = self.parser.parse_args()

        try:
            asistencia_usuario = Asistencia(data['idEstudiante'], data['fecha'])
            asistencia_usuario.Crear()

            return {"mensaje": "Asistencia registrada exitosamente!"}
        except:
            return {"mensaje": "Ocurrio un error al momento de registrar asistencia"}