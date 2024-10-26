from ..calls.municioCalls import MunicipioCalls

class RolServices:
    def ObtenerMunicipios():
        return MunicipioCalls.ObtenerMunicipios()

    def ObtenerMunicipioPorId(id):
        return MunicipioCalls.ObtenerMunicipioPorId(id)
    
    def ObtenerMunicipioPorNombre(nombre):
        return MunicipioCalls.ObtenerMunicipioPorNombre(nombre)