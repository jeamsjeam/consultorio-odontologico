from ..models.cita import Cita

class CitaCalls():

    def ObtenerCitas():
        return Cita.query.all()
