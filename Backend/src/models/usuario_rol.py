from src import db
from sqlalchemy.orm import relationship, backref

class UsuarioRol(db.Model):
    __tablename__ = 'usuario_rol'

    Id = db.Column(db.BigInteger(), primary_key=True)
    usuarioId = db.Column(db.BigInteger(), db.ForeignKey('usuario.Id'))
    rolId = db.Column(db.BigInteger(), db.ForeignKey('rol.Id'))

    def __init__(self, usuarioId, rolId):
        self.usuarioId = usuarioId
        self.rolId = rolId
