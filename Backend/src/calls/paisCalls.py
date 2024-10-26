from ..models.pais import Pais

class PaisCalls():

    def ObtenerPaises():
        return sorted(Pais.query.all(), key=lambda x: x.nombre)

    def ObtenerPaisPorId(id):
        return Pais.query.get(id)
    
    def ObtenerPaisPorNombre(nombre):
        return Pais.query.filter_by(nombre=nombre).first()

