from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.citaServices import CitasServices
from ..schemas.citaSchema import cita_schema,citas_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs
import json
from types import SimpleNamespace

@app.route('/cita', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerCitas():
    respuesta = CitasServices.ObtenerCitas()
    return CustomJsonify(respuesta, cita_schema, citas_schema)

@app.route('/cita/ObtenerPorfecha', methods=['POST'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerCitaPorFecha():
    respuesta = CitasServices.ObtenerCitaPorFecha(json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d)))
    return CustomJsonify(respuesta, cita_schema, citas_schema)

@app.route('/cita/CrearCita', methods=['POST'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def CrearCita():
    respuesta = CitasServices.CrearCita(json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d)))
    return CustomJsonify(respuesta, cita_schema, citas_schema)
