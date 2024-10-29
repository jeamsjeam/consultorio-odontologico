from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.estadoCitaServices import EstadoCitaServices
from ..schemas.estadoCitaSchema import estadoCita_schema,estadosCitas_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/estadoCita', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerEstadoCita():
    respuesta = EstadoCitaServices.ObtenerEstadoCitas()
    return CustomJsonify(respuesta, estadoCita_schema, estadosCitas_schema)
