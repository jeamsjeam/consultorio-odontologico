from ..models.cita import Cita
from src import db
from sqlalchemy import and_, or_, not_

class CitaCalls():

    def ObtenerCitas():
        return Cita.query.all()
    
    def ObtenerCitaPorId(id):
        return Cita.query.get(id)
    
    def ObtenerCitasPorFechaId(fechaId):
        return Cita.query.filter(Cita.fechaId == fechaId).all()
    
    def ObtenerCitasPorPersonaYFecha(personaId, fechaId):
        return Cita.query.filter(and_(Cita.personaId == personaId, Cita.fechaId == fechaId)).first()
    
    def ObtenerCitaPorEstado(estado):
        return Cita.query.filter(Cita.estadoCitaId == estado).all()
    
    def CrearCita(datos):
        try:
            db.session.add(datos)
            db.session.commit()
            db.session.refresh(datos)
            return datos
        
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar cita: {e}")
            raise Exception(f"Error al insertar cita: {e}")

    def ActualizarCita(datos):
        try:
            # Guardar los cambios
            db.session.commit()
            db.session.refresh(datos)
            return datos

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar cita: {e}")
            raise Exception(f"Error al actualizar cita: {e}")