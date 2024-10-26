from src import app
from flask_marshmallow import Marshmallow
from ..models.pais  import Pais

ma = Marshmallow(app)

class PaisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        #load_instance = True
    id = ma.auto_field()
    nombre = ma.auto_field()

pais_schema = PaisSchema()
paises_schema = PaisSchema(many=True)