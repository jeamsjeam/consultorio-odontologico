from src import app
from flask_marshmallow import Marshmallow
from ..models.estado_cita  import EstadoCita

ma = Marshmallow(app)

class EstadoCitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EstadoCita
        load_instance = True

estadoCita_schema = EstadoCitaSchema()
estadosCitas_schema = EstadoCitaSchema(many=True)