from src import db
from sqlalchemy.orm import relationship, backref

class Municipio(db.Model):
    __tablename__ = 'municipio'

    Id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    estadoId = db.Column(db.BigInteger(), db.ForeignKey('estado.Id'))

    def __init__(self, nombre, estadoId):
        self.nombre = nombre
        self.estadoId = estadoId
