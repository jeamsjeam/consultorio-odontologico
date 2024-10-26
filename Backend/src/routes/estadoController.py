from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.estadoServices import EstadoServices
from ..schemas.estadoSchema import estado_schema,estados_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/estado', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerEstados():
    respuesta = EstadoServices.ObtenerEstados()
    return CustomJsonify(respuesta, estado_schema, estados_schema)

@app.route('/estado/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerEstadoPorId(id):
    respuesta = EstadoServices.ObtenerEstadoPorId(id)
    return CustomJsonify(respuesta, estado_schema, estados_schema)

@app.route('/estado/<string:nombre>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerEstadoPorNombre(nombre):
    respuesta = EstadoServices.ObtenerEstadoPorNombre(nombre)
    return CustomJsonify(respuesta, estado_schema, estados_schema)