from ..models.municipio import Municipio

class MunicipioCalls():

    def ObtenerMunicipios():
        return sorted(Municipio.query.all(), key=lambda x: x.nombre)

    def ObtenerMunicipioPorId(id):
        return Municipio.query.get(id)
    
    def ObtenermunicipioPorEstadoId(estadoId):
        return Municipio.query.filter(Municipio.estadoId == estadoId).all()
    
    def ObtenerMunicipioPorNombre(nombre):
        return Municipio.query.filter_by(Municipio.nombre == nombre).first()

