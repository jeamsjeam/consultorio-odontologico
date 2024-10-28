from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from types import SimpleNamespace
from ..services.personaServices import PersonaServices
from ..schemas.personaSchema import persona_schema,personas_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cors
import json


@app.route('/persona', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerPersonas():
    respuesta = PersonaServices.ObtenerPersonas()
    return CustomJsonify(respuesta, persona_schema, personas_schema)
    
@app.route('/persona/<int:cedula>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerPersonaPorCedula(cedula):
    respuesta = PersonaServices.ObtenerPersonaPorCedula(cedula)
    return CustomJsonify(respuesta, persona_schema, personas_schema)

@app.route('/persona/CrearPersona', methods=['POST'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def CrearPersona():
    respuesta = PersonaServices.CrearPersona(json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d)))
    return CustomJsonify(respuesta, persona_schema, personas_schema)