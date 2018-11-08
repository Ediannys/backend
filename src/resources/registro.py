from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.usuario import Usuario

class Registrar(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', help = 'Este campo es requerido', required = True)
    parser.add_argument('apellido', help = 'Este campo es requerido', required = True)
    parser.add_argument('cedula', help = 'Este campo es requerido', required = True)
    parser.add_argument('correo', help = 'Este campo es requerido', required = True)
    parser.add_argument('contraseña', help = 'Este campo es requerido', required = True)

    def post(self):

        data = self.parser.parse_args()

        if Usuario.BuscarCorreo(data['correo']):
            return {'mensaje': 'El usuario {} ya existe'.format(data['correo'])}

        usuario = Usuario(3, data['nombre'], data['apellido'],
            data['cedula'], data['correo'], Usuario.GenerararHash(data['contraseña'])
        )

        try:
            usuario.Crear()
            tokenAcceso = create_access_token(identity = usuario.serialized)
            tokenRefresco = create_refresh_token(identity = usuario.serialized)
            
            return {
                'mensaje': 'El usuario {} fue creado exitosamente'.format(data['correo']),
                'token_acceso': tokenAcceso,
                'token_refresco': tokenRefresco
                }, 201
        except:
            return {'mensaje': 'Ocurrio un problema al intentar crear la cuenta'}, 500

        return data