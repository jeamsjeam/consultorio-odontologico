from ..models.usuario import Usuario
from src import db
from sqlalchemy import and_

class UsuarioCalls():

    def ObtenerUsuarios():
        return sorted(Usuario.query.all(), key=lambda x: x.nombre)

    def AutenticarUsuario(datos):
        return Usuario.query.filter(and_(Usuario.usuario == datos.usuario, Usuario.clave == datos.clave)).first()
    
    def CrearUsuario(datos):
        try:
            existe = Usuario.query.filter(Usuario.usuario == datos.usuario).first()
            
            if existe is not None:
                raise Exception(f"Usuario ya existe")
            
            empleadoNuevo = Usuario(usuario=datos.usuario, 
                                    clave=datos.clave, 
                                    rolId=datos.rolId, 
                                    estado=True)
            db.session.add(empleadoNuevo)
            db.session.commit()
            db.session.refresh(empleadoNuevo)
            return empleadoNuevo
        
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar usuario: {e}")
            raise Exception(f"Error al insertar usuario: {e}")

