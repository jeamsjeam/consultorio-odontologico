from ..calls.estadoCalls import EstadoCalls

class EstadoServices:
    def ObtenerEstados():
        return EstadoCalls.ObtenerEstados()

    def ObtenerEstadoPorId(id):
        return EstadoCalls.ObtenerEstadoPorId(id)
    
    def ObtenerEstadoPorNombre(nombre):
        return EstadoCalls.ObtenerEstadoPorNombre(nombre)