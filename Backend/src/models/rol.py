from src import db
from sqlalchemy.orm import relationship

class Rol(db.Model):
    __tablename__ = 'rol'

    id = db.Column(db.BigInteger(), primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    usuario = relationship('Usuario', backref='rol')

    def __init__(self, nombre):
        self.nombre = nombre
