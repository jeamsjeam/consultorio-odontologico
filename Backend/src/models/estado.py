from src import db
from sqlalchemy.orm import relationship, backref

class Estado(db.Model):
    __tablename__ = 'estado'

    Id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    paisId = db.Column(db.BigInteger(), db.ForeignKey('pais.Id'))

    municipios = relationship('Municipio', backref='estado')

    def __init__(self, nombre, paisId):
        self.nombre = nombre
        self.paisId = paisId
