from src import app
from flask_marshmallow import Marshmallow
from ..models.usuario  import Usuario

ma = Marshmallow(app)

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        #load_instance = True
    id = ma.auto_field()
    usuario = ma.auto_field()
    clave = ma.auto_field()
    estado = ma.auto_field()
    rol = ma.Nested('RolSchema')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)