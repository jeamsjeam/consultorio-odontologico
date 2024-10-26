from ..models.municipio import Municipio

class MunicipioCalls():

    def ObtenerMunicipios():
        return sorted(Municipio.query.all(), key=lambda x: x.nombre)

    def ObtenerMunicipioPorId(id):
        return Municipio.query.get(id)
    
    def ObtenerMunicipioPorNombre(nombre):
        return Municipio.query.filter_by(nombre=nombre).first()

