from ..models.persona import Persona
from src import db
from sqlalchemy import and_, or_, not_

class PersonaCalls():

    def ObtenerPersonas():
        return Persona.query.all()
    
    def ObtenerPersonaPorId(id):
        return Persona.query.get(id)

    def ObtenerPersonaPorCedula(cedula):
        return Persona.query.filter(Persona.cedula == cedula).first()
    
    def ObtenerPersonaPorUsuario(usuarioId):
        return Persona.query.filter(Persona.usuarioId == usuarioId).first()
        
    def CrearPersona(datos):
        try:
            db.session.add(datos)
            db.session.commit()
            db.session.refresh(datos)
            return datos

        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar persona: {e}")
            raise Exception(f"Error al insertar persona: {e}")

    def ActualizarPersona(datos):
        try:
            # Guardar los cambios
            db.session.commit()
            db.session.refresh(datos)
            return datos

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar persona: {e}")
            raise Exception(f"Error al actualizar persona: {e}")



