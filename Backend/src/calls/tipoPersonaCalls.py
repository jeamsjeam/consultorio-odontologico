from ..models.tipo_persona import TipoPersona

class TipoPersonaCalls():

    def ObtenerTipoPersonas():
        return sorted(TipoPersona.query.all(), key=lambda x: x.nombre)

    def ObtenerTipoPersonaPorId(id):
        return TipoPersona.query.get(id)
    
    def ObtenerTipoPersonaPorNombre(nombre):
        return TipoPersona.query.filter_by(nombre=nombre).first()

