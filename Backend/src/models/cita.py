from src import db
from sqlalchemy.orm import relationship, backref

class Cita(db.Model):
    __tablename__ = 'cita'

    id = db.Column(db.BigInteger(), primary_key=True)
    fechaHora = db.Column(db.DateTime, nullable=False) 
    personaId = db.Column(db.BigInteger(), db.ForeignKey('persona.id'))
    servicioId = db.Column(db.BigInteger(), db.ForeignKey('servicio.id'))
    estadoCitaId = db.Column(db.BigInteger(), db.ForeignKey('estado_cita.id'))

    def __init__(self, fechaHora, personaId, servicioId, estadoCitaId):
        self.fechaHora = fechaHora
        self.personaId = personaId
        self.servicioId = servicioId
        self.estadoCitaId = estadoCitaId
