from ..calls.paisCalls import PaisCalls

class PaisServices:
    def ObtenerPaises():
        return PaisCalls.ObtenerPaises()

    def ObtenerPaisPorId(id):
        return PaisCalls.ObtenerPaisPorId(id)
    
    def ObtenerPaisPorNombre(nombre):
        return PaisCalls.ObtenerPaisPorNombre(nombre)