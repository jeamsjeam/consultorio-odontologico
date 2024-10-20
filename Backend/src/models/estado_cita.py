from src import db
from sqlalchemy.orm import relationship, backref

class EstadoCita(db.Model):
    __tablename__ = 'estado_cita'

    Id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    citas = relationship('Cita', backref='estado_cita')

    def __init__(self, nombre):
        self.nombre = nombre
