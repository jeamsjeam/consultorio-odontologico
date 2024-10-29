from ..models.persona import Persona
from src import db
from sqlalchemy import and_, or_, not_

class PersonaCalls():

    def ObtenerPersonas():
        return Persona.query.all()

    def ObtenerPersonaPorCedula(cedula):
        return Persona.query.filter(Persona.cedula == cedula).first()
        
    def CrearPersona(datos):
        try:
            # Crear una instancia de Persona con los atributos filtrados
            nuevo = Persona(**datos)
            db.session.add(nuevo)
            db.session.commit()
            db.session.refresh(nuevo)
            return nuevo

        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar persona: {e}")
            raise Exception(f"Error al insertar persona: {e}")

    def ActualizarPersona(consulta):
        try:
            # Guardar los cambios
            db.session.commit()
            db.session.refresh(consulta)
            return consulta

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar persona: {e}")
            raise Exception(f"Error al actualizar persona: {e}")



