from ..calls.personaCalls import PersonaCalls
from ..models.persona import Persona

class PersonaServices:
    def ObtenerPersonas():
        return PersonaCalls.ObtenerPersonas()

    def ObtenerPersonaPorCedula(cedula):
        return PersonaCalls.ObtenerPersonaPorCedula(cedula)
    
    def CrearPersona(datos):
        return PersonaCalls.CrearPersona(datos)
