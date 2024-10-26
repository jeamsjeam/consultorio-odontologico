from src import app
from flask_marshmallow import Marshmallow
from ..models.tipo_persona  import TipoPersona

ma = Marshmallow(app)

class TipoPersonaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoPersona
        load_instance = True
    # Id = ma.auto_field()
    # nombre = ma.auto_field()

tipoPersona_schema = TipoPersonaSchema()
tipoPersonas_schema = TipoPersonaSchema(many=True)