from src import db
from sqlalchemy.orm import relationship, backref

class TipoPersona(db.Model):
    __tablename__ = 'tipo_persona'

    Id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    personas = relationship('Persona', backref='tipo_persona')

    def __init__(self, nombre):
        self.nombre = nombre
