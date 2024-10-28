from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.paisServices import PaisServices
from ..schemas.paisSchema import pais_schema,paises_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/pais', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerPaises():
    respuesta = PaisServices.ObtenerPaises()
    return CustomJsonify(respuesta, pais_schema, paises_schema)

@app.route('/pais/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerPaisPorId(id):
    respuesta = PaisServices.ObtenerPaisPorId(id)
    return CustomJsonify(respuesta, pais_schema, paises_schema)

@app.route('/pais/PorPais/<int:paisId>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerPaisPorPaisId(paisId):
    respuesta = PaisServices.ObtenerPaisPorPaisId(paisId)
    return CustomJsonify(respuesta, pais_schema, paises_schema)

@app.route('/pais/PorNombre/<string:nombre>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerPaisPorNombre(nombre):
    respuesta = PaisServices.ObtenerPaisPorNombre(nombre)
    return CustomJsonify(respuesta, pais_schema, paises_schema)