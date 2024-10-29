from src import db
from sqlalchemy.orm import relationship, backref

class Cita(db.Model):
    __tablename__ = 'cita'

    id = db.Column(db.BigInteger(), primary_key=True)
    personaId = db.Column(db.BigInteger(), db.ForeignKey('persona.id'))
    servicioId = db.Column(db.BigInteger(), db.ForeignKey('servicio.id'))
    estadoCitaId = db.Column(db.BigInteger(), db.ForeignKey('estado_cita.id'))
    fechaId = db.Column(db.BigInteger(), db.ForeignKey('fecha.id'))

    def __init__(self, personaId, servicioId, estadoCitaId, fechaId):
        self.personaId = personaId
        self.servicioId = servicioId
        self.estadoCitaId = estadoCitaId
        self.fechaId = fechaId
