from ..models.fecha import Fecha

class FechaCalls():

    def ObtenerFechas():
        return Fecha.query.all()
