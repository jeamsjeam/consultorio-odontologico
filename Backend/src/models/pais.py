from src import db
from sqlalchemy.orm import relationship, backref

class Pais(db.Model):
    __tablename__ = 'pais'

    Id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    estados = relationship('Estado', backref='pais')

    def __init__(self, nombre):
        self.nombre = nombre
