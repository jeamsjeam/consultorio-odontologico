from src import app
from flask_marshmallow import Marshmallow
from ..models.usuario  import Usuario

class UsuarioSchema(Marshmallow(app).SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

Usuario_schema = UsuarioSchema()
Usuarios_schema = UsuarioSchema(many=True)