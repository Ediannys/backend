from src.models.base import Base, engine, Session
from src.models.tipo_usuario import TipoUsuario
from src.models.usuario import Usuario
from src.models.curso import Curso
from src.models.seccion import Seccion
from src.models.profesor import Profesor
from src.models.estudiante import Estudiante
from src.models.asistencia import Asistencia
from src.models.pago_curso import PagoCurso

from src.models.prueba import Prueba
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.models.posible_respuesta import PosibleRespuesta
from src.models.prueba_estudiante import PruebaEstudiante
from src.models.certificado import Certificado
from src.models.tokens_revocados import TokensRevocados
from src.models.tokens_inscripcion import TokenInscripcion
from src.models.seed.seed import Seed