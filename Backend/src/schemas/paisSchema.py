from src import app
from flask_marshmallow import Marshmallow
from ..models.pais  import Pais

ma = Marshmallow(app)

class PaisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        load_instance = True

pais_schema = PaisSchema()
paises_schema = PaisSchema(many=True)