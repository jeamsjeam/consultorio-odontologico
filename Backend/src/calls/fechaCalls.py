from ..models.fecha import Fecha
from src import db

class FechaCalls():

    def ObtenerFechas():
        return Fecha.query.all()
    
    def ObtenerFechaPorFecha(fecha):
        return Fecha.query.filter(Fecha.fecha == fecha).first()
    
    def ObtenerFechasPorRango(fechaInicio,fechaFin):
        return Fecha.query.filter(Fecha.fecha.between(fechaInicio, fechaFin)).all()
    
    def CrearFecha(datos):
        try:
            db.session.add(datos)
            db.session.commit()
            db.session.refresh(datos)
            return datos
        
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar fecha: {e}")
            raise Exception(f"Error al insertar fecha: {e}")

