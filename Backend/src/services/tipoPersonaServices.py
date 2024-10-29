from ..calls.tipoPersonaCalls import TipoPersonaCalls

class TipoPersonaServices:
    def ObtenerTipoPersonas():
        return TipoPersonaCalls.ObtenerTipoPersonas()

    def ObtenerTipoPersonaPorId(id):
        return TipoPersonaCalls.ObtenerTipoPersonaPorId(id)
    
    def ObtenerTipoPersonaPorNombre(nombre):
        return TipoPersonaCalls.ObtenerTipoPersonaPorNombre(nombre)