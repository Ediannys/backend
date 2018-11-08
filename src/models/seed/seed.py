from ..base import Base, engine, Session
from ..tipo_usuario import TipoUsuario
from ..usuario import Usuario
from ..curso import Curso
from ..pago_curso import PagoCurso
from ..estudiante import Estudiante
from ..seccion import Seccion


class Seed():
    def seed(self):
        Base.metadata.create_all(engine)
        session = Session()
        
        administrador = TipoUsuario('administrador')
        profesor = TipoUsuario('profesor')
        estudiante = TipoUsuario('estudiante')

        contraseña = Usuario.GenerararHash('admin')
        admin = Usuario(1, 'admin', 'admin', 'admin', 'admin@mail.com', contraseña)


        session.add(administrador)  
        session.add(profesor)
        session.add(estudiante)

        session.add(admin)






        session.commit()
        session.close()