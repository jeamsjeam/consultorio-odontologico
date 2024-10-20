from src import db
from sqlalchemy.orm import relationship, backref

class Usuario(db.Model):
    __tablename__ = 'usuario'

    Id = db.Column(db.BigInteger(), primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Boolean, default=True)  # Estado del usuario (True=activo, False=desactivado)

    persona = relationship('Persona', backref='usuario')

    def __init__(self, cedula, username, contrasena, estado=True):
        self.cedula = cedula
        self.username = username
        self.contrasena = contrasena
        self.estado = estado
