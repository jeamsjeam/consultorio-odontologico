from src import app
from flask_marshmallow import Marshmallow
from ..models.cita  import Cita

ma = Marshmallow(app)

class CitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cita
        #load_instance = True
    id = ma.auto_field()
    persona = ma.Nested('PersonaSchema')
    servicio = ma.Nested('ServicioSchema')
    estado_cita = ma.Nested('EstadoCitaSchema')
    fecha = ma.Nested('FechaSchema')

cita_schema = CitaSchema()
citas_schema = CitaSchema(many=True)