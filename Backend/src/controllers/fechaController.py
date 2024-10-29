from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.fechaServices import FechaServices
from ..schemas.fechaSchema import fecha_schema,fechas_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/fecha', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerFechas():
    respuesta = FechaServices.ObtenerFechas()
    return CustomJsonify(respuesta, fecha_schema, fechas_schema)
