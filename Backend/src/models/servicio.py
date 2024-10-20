from src import db
from sqlalchemy.orm import relationship, backref

class Servicio(db.Model):
    __tablename__ = 'servicio'

    Id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    costo = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.String(150))
    estado = db.Column(db.Boolean, default=True)  # Estado del servicio (True=activo, False=desactivado)

    def __init__(self, nombre, costo, descripcion, estado=True):
        self.nombre = nombre
        self.costo = costo
        self.descripcion = descripcion
        self.estado = estado
