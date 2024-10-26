from src import db
from sqlalchemy.orm import relationship, backref

class Usuario(db.Model):
    __tablename__ = 'usuario'

    Id = db.Column(db.BigInteger(), primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    clave = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Boolean, default=True)  # Estado del usuario (True=activo, False=desactivado)
    rolId = db.Column(db.BigInteger(), db.ForeignKey('rol.Id'))

    persona = relationship('Persona', backref='usuario')

    def __init__(self, usuario, clave, rolId, estado=True):
        self.usuario = usuario
        self.clave = clave
        self.rolId = rolId
        self.estado = estado
