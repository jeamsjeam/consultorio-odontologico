from ..models.estado_cita import EstadoCita

class EstadoCitaCalls():

    def ObtenerEstadoCitas():
        return EstadoCita.query.all()
