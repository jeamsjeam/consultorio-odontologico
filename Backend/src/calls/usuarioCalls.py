from ..models.usuario import Usuario
from src import db
from sqlalchemy import and_, or_, not_

class UsuarioCalls():

    def ObtenerUsuarios():
        return Usuario.query.all()

    def AutenticarUsuario(datos):
        return Usuario.query.filter(and_(Usuario.usuario == datos.usuario, Usuario.clave == datos.clave)).first()
    
    def ObtenerUsuarioPorUsuario(usuario):
        return Usuario.query.filter(Usuario.usuario == usuario).first()

    def CrearUsuario(datos):
        try:
            existe = Usuario.query.filter(Usuario.usuario == datos.usuario).first()
            
            if existe is not None:
                raise Exception(f"Usuario ya existe")
            
            nuevo = Usuario(usuario=datos.usuario, 
                                    clave=datos.clave, 
                                    rolId=datos.rolId, 
                                    estado=True)
            db.session.add(nuevo)
            db.session.commit()
            db.session.refresh(nuevo)
            return nuevo
        
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar usuario: {e}")
            raise Exception(f"Error al insertar usuario: {e}")

