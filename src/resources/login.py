from datetime import timedelta

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.usuario import Usuario

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('correo', help = 'Este campo es requerido', required = True)
    parser.add_argument('contraseña', help = 'Este campo es requerido', required = True)

    def post(self):

        data = self.parser.parse_args()
        usuario = Usuario.BuscarCorreo(data['correo'])
        
        if not usuario:
            return {'mensaje': 'El usuario {} no existe'.format(data['correo'])}
        
        if Usuario.VerificarHash(data['contraseña'], usuario.contraseña):
            
            tokenAcceso = create_access_token(identity = usuario.idTipoUsuario, expires_delta = timedelta(seconds=1200))
            tokenRefresco = create_refresh_token(identity = usuario.serialized)

            return {
                'mensaje': 'Ingreso como {}'.format(usuario.correo),
                "token_acceso": tokenAcceso,
                "token_refresco": tokenRefresco,
                "user": usuario.serialized
            }, 201

        else:
            return {'mensaje': 'Credenciales erradas'}, 500
        
        return data

class IdentificarUsuario(Resource):
    def get(self, idUsuario):
        usuario = Usuario.obtenerUsuario(idUsuario)
        return usuario.serialized