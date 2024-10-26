from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.tipoPersonaServices import TipoPersonaServices
from ..schemas.tipoPersonaSchema import tipoPersona_schema,tipoPersonas_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/tipoPersona', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerTipoPersonas():
    respuesta = TipoPersonaServices.ObtenerTipoPersonas()
    return CustomJsonify(respuesta, tipoPersona_schema, tipoPersonas_schema)

@app.route('/tipoPersona/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerTipoPersonaPorId(id):
    respuesta = TipoPersonaServices.ObtenerTipoPersonaPorId(id)
    return CustomJsonify(respuesta, tipoPersona_schema, tipoPersonas_schema)

@app.route('/tipoPersona/<string:nombre>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerTipoPersonaPorNombre(nombre):
    respuesta = TipoPersonaServices.ObtenerTipoPersonaPorNombre(nombre)
    return CustomJsonify(respuesta, tipoPersona_schema, tipoPersonas_schema)