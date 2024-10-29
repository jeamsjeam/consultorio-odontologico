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
            # Filtrar solo los atributos válidos para el modelo Persona
            atributos_validos = {key: value for key, value in datos.__dict__.items() if hasattr(Persona, key) and value is not None}

            # Crear una instancia de Persona con los atributos filtrados
            nuevo = Persona(**atributos_validos)
            db.session.add(nuevo)
            db.session.commit()
            db.session.refresh(nuevo)
            return nuevo

        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar persona: {e}")
            raise Exception(f"Error al insertar persona: {e}")

    def ActualizarPersona(consulta, datos):
        try:
            # Recorrer todos los atributos de 'datos' y asignarlos si existen en consulta, excluyendo 'id'
            for key, value in datos.__dict__.items():
                if key != 'id' and hasattr(consulta, key) and value is not None:
                    setattr(consulta, key, value)

            # Guardar los cambios
            db.session.commit()
            db.session.refresh(consulta)
            return consulta

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar persona: {e}")
            raise Exception(f"Error al actualizar persona: {e}")



