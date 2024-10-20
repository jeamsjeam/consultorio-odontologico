from src import app
from flask_marshmallow import Marshmallow
from ..models.rol  import Rol

ma = Marshmallow(app)

class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True
        #fields = ('id', 'nombre') # fields to expose

rol_schema = RolSchema()
roles_schema = RolSchema(many=True)