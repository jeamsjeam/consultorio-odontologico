from ..models.estado_cita import EstadoCita

class EstadoCitaCalls():

    def ObtenerEstadoCitas():
        return EstadoCita.query.all()
    
    def ObtenerEstadoCitaPorNombre(nombre):
        return EstadoCita.query.filter(EstadoCita.nombre == nombre).first()
