from src import app
from flask_marshmallow import Marshmallow
from ..models.municipio  import Municipio

ma = Marshmallow(app)

class MunicipioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Municipio
        #load_instance = True
    Id = ma.auto_field()
    nombre = ma.auto_field()
    rol = ma.Nested('EstadoSchema')

municipio_schema = MunicipioSchema()
municipios_schema = MunicipioSchema(many=True)