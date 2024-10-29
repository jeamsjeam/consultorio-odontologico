from ..models.servicio import Servicio

class ServicioCalls():

    def ObtenerServicios():
        return Servicio.query.all()
