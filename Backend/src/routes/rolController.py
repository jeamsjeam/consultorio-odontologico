from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from ..services.rolServices import RolServices
from ..schemas.rolSchema import roles_schema,rol_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cors

@app.route('/rol', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerRoles():
    respuesta = RolServices.ObtenerRoles()
    return CustomJsonify(respuesta, rol_schema, roles_schema)

@app.route('/rol/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerRolPorId(id):
    respuesta = RolServices.ObtenerRolPorId(id)
    return CustomJsonify(respuesta, rol_schema, roles_schema)