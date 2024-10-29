from src import db
from sqlalchemy.orm import relationship, backref

class Fecha(db.Model):
    __tablename__ = 'fecha'

    id = db.Column(db.BigInteger(), primary_key=True)
    fecha = db.Column(db.Date, nullable=False) 
    cantidad = db.Column(db.Integer, nullable=False)

    citas = relationship('Cita', backref='fecha')

    def __init__(self, fecha, cantidad):
        self.fecha = fecha
        self.cantidad = cantidad
