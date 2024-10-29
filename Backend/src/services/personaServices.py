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
