import datetime
from datetime import date
from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.usuario import Usuario
from src.models.curso import Curso
from src.models.pago_curso import PagoCurso
from src.models.prueba import Prueba
from src.models.seccion import Seccion
from src.models.prueba_estudiante import PruebaEstudiante
from src.models.estudiante import Estudiante

class AgregarEstudiante(Resource):
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

        usuario = Usuario(3, data['nombre'], data['apellido'],
                          data['cedula'], data['correo'], Usuario.GenerararHash(data['contraseña'])
                          )

        try:
            usuario.Crear()
            tokenAcceso = create_access_token(identity=usuario.serialized)
            tokenRefresco = create_refresh_token(identity=usuario.serialized)

            return {
                       'mensaje': 'El estudiante {} fue creado exitosamente'.format(data['correo']),
                       'token_acceso': tokenAcceso,
                       'token_refresco': tokenRefresco
                   }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar crear estudiante'}, 500
        return data

class AgregarPago_curso(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('idUsuario', help='Este campo es requerido', required=True)
    parser.add_argument('idCurso', help='Este campo es requerido', required=True)
    parser.add_argument('nTransferencia', help='Este campo es requerido', required=True)
    parser.add_argument('monto', help='Este campo es requerido', required=True)
    parser.add_argument('fechaPago', help='Este campo es requerido', required=True)

    def post(self):

        data = self.parser.parse_args()
        pago_curso = PagoCurso(data['idUsuario'], data['idCurso'], data['nTransferencia'], data['monto'],
                                   data['fechaPago'])
        try:
            pago_curso.Crear()
            return {
                           'mensaje': 'Se agrego un curso al profesor con exito'
                    }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar agregar el curso'}, 500

        return data

class ObtenerEstudiante(Resource):
    def get(self, id):
        estudiante = Usuario.obtenerEstudiante(id)
        if estudiante is None:
            return { 'mensaje': 'Ocurrio un problema al intentar regresar estudiante'}, 500

        return estudiante

class MostrarCursosEstudiante(Resource):
    def get(self, idEstudiante):

        todos_cursos = Curso.obtenerCursos()
        idPrueba = PruebaEstudiante.obtenerIdPrueba(idEstudiante)
        cursos_preinscritos = []
        cursos = []
        cont = 0
        
        if idPrueba == []:
            return Curso.MostrarCursos_2()

        for i in range(0, len(idPrueba)):
            cursos_preinscritos.append(Prueba.obtenerCurso(idPrueba[i].idPrueba))

        for i in range(0, len(todos_cursos)):
            secciones = Seccion.obtenerSecciones(todos_cursos[i].id)
            if len(secciones) > 0:
                cont = 0
                for j in range(0, len(cursos_preinscritos)):
                    if todos_cursos[i].id == cursos_preinscritos[j].idCurso:
                        cont = cont + 1
                if cont == 0:
                    curso = {
                        "id": todos_cursos[i].id,
                        "nombre": todos_cursos[i].nombre,
                        "descripcion": todos_cursos[i].descripcion,
                        "fechaInicio": todos_cursos[i].fechaInicio,
                        "fechaFinal": todos_cursos[i].fechaFinal,
                        "precio": todos_cursos[i].precio
                    }
                    cursos.append(curso)

        return jsonify(cursos)

class Examen(Resource):
    def get(self, idCurso):
        prueba = Prueba.obtenerPrueba(idCurso)
        return prueba

class Calificar(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('pregunta', type=dict, action='append')

    def post(self, idCurso):
        args = self.parser.parse_args()
        calificacion = 0
        aprobacion = False
        respuestas = Prueba.calificar(idCurso)

        for i in range(0, len(respuestas)):
            for j in range(0, len(args['pregunta'])):
                if respuestas[i]['idPregunta'] == args['pregunta'][j]['pregunta']:
                    if respuestas[i]['idRespuesta'] == args['pregunta'][j]['respuesta']:
                        calificacion = calificacion + respuestas[i]['ponderacion']
                        print(calificacion)

                        if calificacion >= 70 and calificacion <= 100:
                            aprobacion = True

        return {
                    "calificacion": calificacion, 
                    "aprobacion": aprobacion
                }

class RegistrarExamen(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('idEstudiante', help='Este campo es requerido', required=True)
    parser.add_argument('idPrueba', help='Este campo es requerido', required=True)
    parser.add_argument('calificacion', help='Este campo es requerido', required=True)

    def post(self):
        data = self.parser.parse_args()
        prueba_estudiante = PruebaEstudiante(data['idEstudiante'], 
                                                data['idPrueba'], data['calificacion'])

        if PruebaEstudiante.existe(data['idEstudiante'], data['idPrueba']) is None:
            prueba_estudiante.Crear()
            print(data)
            return {"mensaje": "Examen registrado exitosamente!"}

        return {"mensaje":"Error! ya este usuario presento esta prueba"}

class Inscripcion(Resource):

    def get(self, idEstudiante):
        return PruebaEstudiante.obtenerCursosPreInscritos(idEstudiante)

class PagarCurso(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('idUsuario', help='Este campo es requerido', required=True)
    parser.add_argument('idCurso', help='Este campo es requerido', required=True)
    parser.add_argument('seccion', help='Este campo es requerido', required=True)
    parser.add_argument('monto', help='Este campo es requerido', required=True)
    parser.add_argument('fecha', help='Este campo es requerido', required=True)
    parser.add_argument('nTransferencia', help='Este campo es requerido', required=True)

    def post(self):
        
        data = self.parser.parse_args()
        existeTransferencia = PagoCurso.verificarTransferencia(data['nTransferencia'])

        if existeTransferencia is None:
            try:
                pago_curso = PagoCurso(data['idUsuario'], data['idCurso'], 
                                        data['nTransferencia'], data['monto'], data['fecha'])
                pago_curso.Crear()

                estudiante = Estudiante(data['idUsuario'], data['idCurso'], data['seccion'], False)
                estudiante.Crear()

                return {"mensaje":"Curso pagado/inscrito exitosamente"}

            except:
                return {'mensaje': 'Ocurrio un problema al intentar pagar curso'}, 500

        return data



