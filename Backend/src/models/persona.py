from src import db
from sqlalchemy.orm import relationship, backref

class Persona(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.BigInteger(), primary_key=True)
    cedula = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    municipioId = db.Column(db.BigInteger(), db.ForeignKey('municipio.id'))
    tipoPersonaId = db.Column(db.BigInteger(), db.ForeignKey('tipo_persona.id'))
    usuarioId = db.Column(db.BigInteger(), db.ForeignKey('usuario.id'))
    
    def __init__(self, nombre, apellido, cedula, telefono, direccion, municipioId, tipoPersonaId, usuarioId):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.telefono = telefono
        self.direccion = direccion
        self.municipioId = municipioId
        self.tipoPersonaId = tipoPersonaId
        self.usuarioId = usuarioId
