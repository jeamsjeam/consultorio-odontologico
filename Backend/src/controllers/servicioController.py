from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.servicioServices import ServicioServices
from ..schemas.servicioSchema import servicio_schema,servicios_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cosrs

@app.route('/servicio', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerServicios():
    respuesta = ServicioServices.ObtenerServicios()
    return CustomJsonify(respuesta, servicio_schema, servicios_schema)