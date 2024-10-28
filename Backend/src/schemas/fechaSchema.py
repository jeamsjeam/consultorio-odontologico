from src import app
from flask_marshmallow import Marshmallow
from ..models.fecha  import Fecha

ma = Marshmallow(app)

class FechaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Fecha
        load_instance = True

fecha_schema = FechaSchema()
fechas_schema = FechaSchema(many=True)