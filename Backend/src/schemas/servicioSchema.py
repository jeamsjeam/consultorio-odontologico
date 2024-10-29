from src import app
from flask_marshmallow import Marshmallow
from ..models.servicio  import Servicio

ma = Marshmallow(app)

class ServicioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Servicio
        load_instance = True

servicio_schema = ServicioSchema()
servicios_schema = ServicioSchema(many=True)