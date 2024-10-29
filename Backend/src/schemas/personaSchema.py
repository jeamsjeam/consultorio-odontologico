from src import app
from flask_marshmallow import Marshmallow
from ..models.persona  import Persona

ma = Marshmallow(app)

class PersonaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Persona
        #load_instance = True
    id = ma.auto_field()
    cedula = ma.auto_field()
    nombre = ma.auto_field()
    apellido = ma.auto_field()
    telefono = ma.auto_field()
    direccion = ma.auto_field()
    usuario = ma.Nested('UsuarioSchema')
    municipio = ma.Nested('MunicipioSchema')
    tipo_persona = ma.Nested('TipoPersonaSchema')

persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True)