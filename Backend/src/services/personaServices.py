from ..calls.personaCalls import PersonaCalls
from ..models.persona import Persona

class PersonaServices:
    def ObtenerPersonas():
        return PersonaCalls.ObtenerPersonas()

    def ObtenerPersonaPorCedula(cedula):
        return PersonaCalls.ObtenerPersonaPorCedula(cedula)
    
    def CrearPersona(datos):
        try:
            existe = PersonaCalls.ObtenerPersonaPorCedula(datos.cedula)
            if existe is not None:
                    raise Exception(f"Persona registrada")
                
            return PersonaCalls.CrearPersona(datos)
        except Exception as e:
            print(f"Error al insertar persona: {e}")
            raise Exception(f"Error al insertar persona: {e}")
    
    def ActualizarPersona(datos):
        try:
            # Validar que el id esté presente, no sea None y sea positivo
            if not hasattr(datos, 'id') or datos.id is None or datos.id < 0:
                raise Exception("ID de la persona no proporcionado o inválido")

            # Comprobar que la persona exista en la base de datos
            consulta = Persona.query.get(datos.id)
            if not consulta:
                raise Exception("Persona no encontrada")
            
            # Llamar a la función de actualización si la validación es exitosa
            return PersonaCalls.ActualizarPersona(consulta, datos)
        except Exception as e:
            print(f"Error al actualizar persona: {e}")
            raise Exception(f"Error al actualizar persona: {e}")
