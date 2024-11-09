from ..calls.personaCalls import PersonaCalls
from ..models.persona import Persona

class PersonaServices:
    def ObtenerPersonas():
        return PersonaCalls.ObtenerPersonas()

    def ObtenerPersonaPorCedula(cedula):
        return PersonaCalls.ObtenerPersonaPorCedula(cedula)
    
    def ObtenerPersonaPorUsuario(usuarioId):
        return PersonaCalls.ObtenerPersonaPorUsuario(usuarioId)
    
    def CrearPersona(datos):
        try:
            # Se verifica si existe un registro con la misma cedula
            existe = PersonaCalls.ObtenerPersonaPorCedula(datos.cedula)
            if existe is not None:
                raise Exception(f"Persona registrada")
                
             # Filtrar solo los atributos válidos para el modelo Persona
            atributosValidos = {key: value for key, value in datos.__dict__.items() if hasattr(Persona, key) and value is not None}
            
            # Crear una instancia de Persona con los atributos filtrados
            nuevo = Persona(**atributosValidos)

            return PersonaCalls.CrearPersona(nuevo)
        except Exception as e:
            print(f"Error al insertar persona: {e}")
            raise Exception(f"Error al insertar persona: {e}")
    
    def ActualizarPersona(datos):
        try:
            # Validar que el id esté presente, no sea None y sea positivo
            if not hasattr(datos, 'cedula') or datos.cedula is None or datos.cedula < 0:
                raise Exception("Cedula de la persona no proporcionado o inválido")

            # Comprobar que la persona exista en la base de datos
            consulta = PersonaCalls.ObtenerPersonaPorCedula(datos.cedula)
            if not consulta:
                raise Exception("Persona no encontrada")
            
            # Recorrer todos los atributos de 'datos' y asignarlos si existen en consulta, excluyendo 'id'
            for key, value in datos.__dict__.items():
                if key != 'id' and key != 'cedula' and hasattr(consulta, key) and value is not None:
                    setattr(consulta, key, value)

            # Llamar a la función de actualización si la validación es exitosa
            return PersonaCalls.ActualizarPersona(consulta)
        except Exception as e:
            print(f"Error al actualizar persona: {e}")
            raise Exception(f"Error al actualizar persona: {e}")
