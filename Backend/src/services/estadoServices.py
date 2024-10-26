from ..calls.estadoCalls import EstadoCalls

class EstadoServices:
    def ObtenerEstados():
        return EstadoCalls.ObtenerEstados()

    def ObtenerEstadoPorId(id):
        return EstadoCalls.ObtenerEstadoPorId(id)
    
    def ObtenerEstadoPorPaisId(nombre):
        return EstadoCalls.ObtenerEstadoPorPaisId(nombre)
    
    def ObtenerEstadoPorNombre(nombre):
        return EstadoCalls.ObtenerEstadoPorNombre(nombre)