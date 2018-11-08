import datetime
from datetime import date
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.usuario import Usuario
from src.models.curso import Curso
from src.models.profesor import Profesor
from src.models.seccion import Seccion
from src.models.pago_curso import PagoCurso
from src.models.estudiante import Estudiante
from src.models.prueba import Prueba
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.models.posible_respuesta import PosibleRespuesta

class AgregarProfesor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', help='Este campo es requerido', required=True)
    parser.add_argument('apellido', help='Este campo es requerido', required=True)
    parser.add_argument('cedula', help='Este campo es requerido', required=True)
    parser.add_argument('correo', help='Este campo es requerido', required=True)
    parser.add_argument('contraseña', help='Este campo es requerido', required=True)

    def post(self):

        data = self.parser.parse_args()

        if Usuario.BuscarCorreo(data['correo']):
            return {'mensaje': 'El profesor {} ya existe'.format(data['correo'])}

        usuario = Usuario(2, data['nombre'], data['apellido'],
                          data['cedula'], data['correo'], Usuario.GenerararHash(data['contraseña'])
                          )

        try:
            usuario.Crear()
            tokenAcceso = create_access_token(identity=usuario.serialized)
            tokenRefresco = create_refresh_token(identity=usuario.serialized)

            return {
                       'mensaje': 'El profesor {} fue creado exitosamente'.format(data['correo']),
                       'token_acceso': tokenAcceso,
                       'token_refresco': tokenRefresco
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar crear profesor'}, 500
        return data

class AgregarCurso(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', help='Este campo es requerido', required=True)
    parser.add_argument('descripcion', help='Este campo es requerido', required=True)
    parser.add_argument('inicia', help='Este campo es requerido', required=True)
    parser.add_argument('finaliza', help='Este campo es requerido', required=True)
    parser.add_argument('precio', help='Este campo es requerido', required=True)

    def post(self):

        data = self.parser.parse_args()

        if Curso.Buscar(data['nombre']):
            return {'mensaje': 'El curso {} ya existe'.format(data['nombre'])}

        curso = Curso(data['nombre'], data['descripcion'],
                      data['inicia'],
                      data['finaliza'],
                      data['precio']
                      )

        try:
            curso.Crear()

            return {
                       'mensaje': 'El curso {} fue creado exitosamente'.format(data['nombre'])
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar crear curso'}, 500

        return data

class AgregarCursoProfesor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('idUsuario', help='Este campo es requerido', required=True)
    parser.add_argument('idCurso', help='Este campo es requerido', required=True)
    parser.add_argument('nCupos', help='Este campo es requerido', required=True)
    parser.add_argument('seccion', help='Este campo es requerido', required=True)

    def post(self):

        data = self.parser.parse_args()

        nombre= Profesor.BuscarNombre(data['idCurso'])

        if Profesor.BuscarNombreYseccion(nombre, data['seccion']):
            return {'mensaje': 'Error, el curso {} ya se encuentra asociado a la seccion {}'.format(nombre, data['seccion'])}

        seccion = Seccion(data['idCurso'], data['nCupos'], data['nCupos'], data['seccion'])

        try:
            seccion.Crear()
            profesor = Profesor(data['idUsuario'], data['idCurso'], seccion.id)
            profesor.Crear()

            return {
                       'mensaje': 'Se agrego un curso al profesor con exito'
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar agregar el curso'}, 500

        return data


class AgregarPregunta(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pregunta', help='Este campo es requerido', required=True)
    parser.add_argument('ponderacion', help='Este campo es requerido', required=True)

    def post(self, id):
        data = self.parser.parse_args()

        prueba = Prueba.BuscarCurso(id)
        curso = Curso.BuscarPorId(id)
        if prueba:
            bandera = 0

        else:
            bandera = 1
            prueba = Prueba(id, curso.nombre)

        try:
            if bandera == 1:
                prueba.Crear()

            pregunta = Pregunta(prueba.id, data['pregunta'], data['ponderacion'])
            pregunta.Crear()

            return {
                       'mensaje': 'Se agrego una pregunta a la prueba con exito'
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar agregar la pregunta a la prueba'}, 500
        return data

class AgregarRespuesta(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('idPrueba', help='Este campo es requerido', required=True)
    parser.add_argument('respuesta', help='Este campo es requerido', required=True)

    def post(self, id):
        data = self.parser.parse_args()
        try:
            respuesta = Respuesta(data['idPrueba'], id, data['respuesta'])
            respuesta.Crear()
            return {
                       'mensaje': 'Se agrego una respuesta a la pregunta con exito'
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar agregar la respuesta a la pregunta'}, 500
        return data

class AgregarPosibleRespuesta(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('respuesta', help='Este campo es requerido', required=True)

    def post(self, id):
        data = self.parser.parse_args()

        try:
            posible_respuesta = PosibleRespuesta(id, data['respuesta'])
            posible_respuesta.Crear()
            return {
                       'mensaje': 'Se agrego una respuesta a la pregunta con exito'
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar agregar la respuesta a la pregunta'}, 500
        return data



class AprobarTransferencia(Resource):
    def put(self, id):
        return PagoCurso.AprobarTransferencia(id)

class AprobarEnvio(Resource):
    def put(self, id):
        return Estudiante.AprobarEnvio(id)

class MostrarPagos_curso(Resource):
    def get(self, id):
        return PagoCurso.MostrarPagos(id)

class MostrarProfesores(Resource):
    def get(self):
        return Usuario.MostrarUsuarios(2)

class MostrarCursos(Resource):
    def get(self):
        return Curso.MostrarCursos()

class MostrarPreguntas(Resource):
    def get(self, id):
        try:
            return Pregunta.MostrarPreguntas(id)
        except:
            return {'mensaje': 'No hay preguntas para mostrar'}, 500

class MostrarRespCorr(Resource):
    def get(self, id):
        try:
            return Respuesta.MostrarRespuestas(id)
        except:
            return {'mensaje': 'No hay respuestas para mostrar'}, 500


class MostrarPosResp(Resource):
    def get(self, id):
        try:
            return PosibleRespuesta.MostrarRespuestas(id)
        except:
            return {'mensaje': 'No hay respuestas para mostrar'}, 500

class MostrarPregunta(Resource):
    def get(self, id):
        try:
            return Pregunta.MostrarPregunta(id)
        except:
            return {'mensaje': 'No existe esa pregunta'}, 500


class MostrarEstAprobados(Resource):
    def get(self, id):
        return Estudiante.MostrarEstAprobados(id)

class EliminarProfesor(Resource):
    def delete(self, id):
        eliminado = Usuario.EliminarUsuario(id)
        return eliminado

class EliminarCurso(Resource):
    def delete(self, id):
        try:
            eliminado = Curso.EliminarCurso(id)
            return {
                       'mensaje': 'Se agrego elimino el curso con exito'
                   }, 201
        except:
            return {'mensaje': 'No se puede eliminar el curso'}, 500

class EliminarPregunta(Resource):
    def delete(self, id):
        eliminado = Pregunta.EliminarPregunta(id)
        return eliminado


class EliminarRespCorr(Resource):
    def delete(self, id):
        eliminado = Respuesta.EliminarRespuesta(id)
        return eliminado

class EliminarPosibleRespuesta(Resource):
    def delete(self, id):
        eliminado = PosibleRespuesta.EliminarPosibleRespuesta(id)
        return eliminado

class ModificarPregunta(Resource):
    def put(self, id):
        modificado = Pregunta.ModificarPregunta(id)
        return modificado

class ModificarRespCorr(Resource):
    def put(self, id):
        modificado = Respuesta.ModificarRespuesta(id)
        return modificado

class ModificarPosResp(Resource):
    def put(self, id):
        modificado = PosibleRespuesta.ModificarRespuesta(id)
        return modificado

class ModificarPosibleRespuesta(Resource):
    def put(self, id):
        modificado = Pregunta.ModificarPregunta(id)
        return modificado

class ModificarProfesor(Resource):
    def get(self, id):
        modificado = Usuario.ModificarUsuario(id)
        return modificado

class ModificarCurso(Resource):
    def put(self, id):
        modificado = Curso.ModificarCurso(id)
        return modificado

