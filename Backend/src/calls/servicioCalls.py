from ..models.servicio import Servicio

class ServicioCalls():

    def ObtenerServicios():
        return Servicio.query.all()
    
    def ObtenerServicioPorId(id):
        return Servicio.query.get(id)
