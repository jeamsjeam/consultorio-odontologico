from src import db
from sqlalchemy.orm import relationship, backref

class Pais(db.Model):
    __tablename__ = 'pais'

    id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    estado = relationship('Estado', backref='pais')

    def __init__(self, nombre):
        self.nombre = nombre
