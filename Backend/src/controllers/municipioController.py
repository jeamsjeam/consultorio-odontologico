from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.municipioServices import MunicipioServices
from ..schemas.municipioSchema import municipio_schema,municipios_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/municipio', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerMunicipios():
    respuesta = MunicipioServices.ObtenerMunicipios()
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)

@app.route('/municipio/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerMunicipioPorId(id):
    respuesta = MunicipioServices.ObtenerMunicipioPorId(id)
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)

@app.route('/municipio/PorEstado/<int:estadoId>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenermunicipioPorEstadoId(estadoId):
    respuesta = MunicipioServices.ObtenermunicipioPorEstadoId(estadoId)
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)

@app.route('/municipio/PorNombre/<string:nombre>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerMunicipioPorNombre(nombre):
    respuesta = MunicipioServices.ObtenerMunicipioPorNombre(nombre)
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)