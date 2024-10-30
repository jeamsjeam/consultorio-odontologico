from ..models.usuario import Usuario
from src import db
from sqlalchemy import and_, or_, not_

class UsuarioCalls():

    def ObtenerUsuarios():
        return Usuario.query.all()
    
    def ObtenerUsuarioPorId(id):
        return Usuario.query.get(id)

    def AutenticarUsuario(datos):
        return Usuario.query.filter(and_(Usuario.usuario == datos.usuario, Usuario.clave == datos.clave)).first()
    
    def ObtenerUsuarioPorUsuario(usuario):
        return Usuario.query.filter(Usuario.usuario == usuario).first()

    def CrearUsuario(datos):
        try:
            db.session.add(datos)
            db.session.commit()
            db.session.refresh(datos)
            return datos
        
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar usuario: {e}")
            raise Exception(f"Error al insertar usuario: {e}")

    def ActualizarUsuario(datos):
        try:
            # Guardar los cambios
            db.session.commit()
            db.session.refresh(datos)
            return datos

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar usuario: {e}")
            raise Exception(f"Error al actualizar usuario: {e}")
