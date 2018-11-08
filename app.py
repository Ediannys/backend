from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Configuracion de mensajes
from flask import render_template
from flask_mail import Mail, Message
import pdfkit
import jinja2

from src.models.seed.seed import Seed
from src.resources.registro import Registrar
from src.resources.login import Login
from src.resources.login import IdentificarUsuario

from src.resources.administrador import AgregarProfesor
from src.resources.administrador import MostrarProfesores
from src.resources.administrador import EliminarProfesor
from src.resources.administrador import ModificarProfesor
from src.resources.administrador import AgregarCurso
from src.resources.administrador import MostrarCursos
from src.resources.administrador import EliminarCurso
from src.resources.administrador import AgregarCursoProfesor
from src.resources.administrador import MostrarPagos_curso
from src.resources.administrador import AprobarTransferencia

from src.resources.estudiante import AgregarEstudiante
from src.resources.estudiante import AgregarPago_curso
from src.resources.estudiante import ObtenerEstudiante

from src.resources.administrador import MostrarEstAprobados
from src.resources.administrador import AgregarPregunta
from src.resources.administrador import AgregarRespuesta
from src.resources.administrador import AgregarPosibleRespuesta
from src.resources.administrador import EliminarPregunta
from src.resources.administrador import EliminarRespCorr
from src.resources.administrador import EliminarPosibleRespuesta
from src.resources.administrador import ModificarPregunta
from src.resources.administrador import ModificarCurso
from src.resources.administrador import MostrarPreguntas
from src.resources.administrador import MostrarPregunta
from src.resources.administrador import MostrarRespCorr
from src.resources.administrador import ModificarRespCorr
from src.resources.administrador import MostrarPosResp
from src.resources.administrador import ModificarPosResp
from src.resources.administrador import AprobarEnvio

from src.resources.estudiante import MostrarCursosEstudiante
from src.resources.estudiante import Examen
from src.resources.estudiante import Calificar
from src.resources.estudiante import RegistrarExamen
from src.resources.estudiante import Inscripcion
from src.resources.estudiante import PagarCurso


from src.resources.profesor import CursoSeccion
from src.resources.profesor import EstudianteSeccion
from src.resources.profesor import CalificarEstudiante
from src.resources.profesor import RegistrarAsistencia

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

#configuracion de mensajes
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('src/templates'),
])
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cursosweb.aem@gmail.com'
app.config['MAIL_PASSWORD'] = 'desarrollo1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)

# Insertando tipos de usuarios
# Solo se usa una vez, es solo para crear tipos de usuario y administrador
# seed = Seed()
# seed.seed()

# Endpoints para el FrontEnd

# Home
api.add_resource(Registrar, '/registro')
api.add_resource(Login, '/login')
api.add_resource(IdentificarUsuario, '/identificar_usuario/<idUsuario>')

# Administrador
api.add_resource(AgregarProfesor, '/agregar_p')
api.add_resource(AgregarCurso, '/agregar_c')
api.add_resource(MostrarProfesores, '/mostrar_p')
api.add_resource(MostrarCursos, '/mostrar_c')
api.add_resource(EliminarProfesor, '/eliminar_p/<id>', methods=["DELETE"])
api.add_resource(EliminarCurso, '/eliminar_c/<id>', methods=["DELETE"])
api.add_resource(ModificarProfesor, '/modificar_p/<id>')
api.add_resource(AgregarCursoProfesor, '/agregar_cp')
api.add_resource(AgregarEstudiante, '/agregar_e')
api.add_resource(AgregarPago_curso, '/agregar_pago_c')
api.add_resource(MostrarPagos_curso, '/mostrar_pagos_c/<id>')
api.add_resource(ObtenerEstudiante, '/obtener_estudiante/<id>')
api.add_resource(AprobarTransferencia, '/aprobar_transf/<id>')
api.add_resource(MostrarEstAprobados, '/mostrar_est_aprob/<id>')
api.add_resource(AgregarPregunta, '/agregar_pregunta/<id>')
api.add_resource(AgregarRespuesta, '/agregar_resp_corr/<id>')
api.add_resource(AgregarPosibleRespuesta, '/agregar_pos_resp/<id>')
api.add_resource(EliminarPregunta, '/eliminar_pregunta/<id>')
api.add_resource(EliminarRespCorr, '/eliminar_resp_corr/<id>')
api.add_resource(EliminarPosibleRespuesta, '/eliminar_pos_resp/<id>')
api.add_resource(ModificarPregunta, '/modificar_pregunta/<id>')
api.add_resource(ModificarCurso, '/modificar_c/<id>')
api.add_resource(MostrarPreguntas, '/mostrar_preguntas/<id>')
api.add_resource(MostrarPregunta, '/mostrar_pregunta/<id>')
api.add_resource(MostrarRespCorr, '/mostrar_resp_corr/<id>')
api.add_resource(ModificarRespCorr, '/modificar_resp_corr/<id>')
api.add_resource(MostrarPosResp, '/mostrar_pos_resp/<id>')
api.add_resource(ModificarPosResp, '/modificar_pos_resp/<id>')
api.add_resource(AprobarEnvio, '/aprobar_envio/<id>')


# Estudiante
api.add_resource(MostrarCursosEstudiante, '/mostrar_c/<idEstudiante>')
api.add_resource(Examen, '/examen/<idCurso>')
api.add_resource(Calificar, '/calificar/<idCurso>', methods=["POST"])
api.add_resource(RegistrarExamen, '/registrar_examen')
api.add_resource(Inscripcion, '/inscripcion/<idEstudiante>')
api.add_resource(PagarCurso, '/pagar_curso')

# Profesor
api.add_resource(CursoSeccion, '/cursos_secciones/<idProfesor>')
api.add_resource(EstudianteSeccion, '/mostrar_estudiantes/<idSeccion>')
api.add_resource(CalificarEstudiante, '/calificar')
api.add_resource(RegistrarAsistencia, '/asistencia')


@app.route('/')
def index():
    return 'Server Running :)'

@app.route("/enviar_pdf/<username>/<course>/<correo>", methods=['GET'])
def enviar_pdf(username, course, correo):
     rendered= render_template('pdf_certificado.html', username=username, course=course )
     pdf= pdfkit.from_string(rendered, False)
     msg = Message(subject="Hello", sender=app.config.get("MAIL_USERNAME"),recipients=["ediannys.16@gmail.com"])
     msg.attach("result.pdf", "application/pdf", pdf)
     mail.send(msg)

if __name__ == '__main__':
    mail.init_app(app)
    app.run(debug=True)