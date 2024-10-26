from ..models.estado import Estado

class EstadoCalls():

    def ObtenerEstados():
        return sorted(Estado.query.all(), key=lambda x: x.nombre)

    def ObtenerEstadoPorId(id):
        return Estado.query.get(id)
    
    def ObtenerEstadoPorNombre(nombre):
        return Estado.query.filter_by(nombre=nombre).first()

