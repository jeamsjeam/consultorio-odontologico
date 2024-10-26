from ..models.estado import Estado

class EstadoCalls():

    def ObtenerEstados():
        return sorted(Estado.query.all(), key=lambda x: x.nombre)

    def ObtenerEstadoPorId(id):
        return Estado.query.get(id)
    
    def ObtenerEstadoPorPaisId(paisId):
        return Estado.query.filter_by(paisId=paisId).all()
    
    def ObtenerEstadoPorNombre(nombre):
        return Estado.query.filter_by(nombre=nombre).first()

