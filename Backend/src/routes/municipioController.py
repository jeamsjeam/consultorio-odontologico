from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.municipioServices import MunicipioCalls
from ..schemas.municipioSchema import municipio_schema,municipios_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cors

@app.route('/municipio', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerMunicipios():
    respuesta = MunicipioCalls.ObtenerMunicipios()
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)

@app.route('/municipio/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerMunicipioPorId(id):
    respuesta = MunicipioCalls.ObtenerMunicipioPorId(id)
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)

@app.route('/municipio/<string:nombre>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerMunicipioPorNombre(nombre):
    respuesta = MunicipioCalls.ObtenerMunicipioPorNombre(nombre)
    return CustomJsonify(respuesta, municipio_schema, municipios_schema)