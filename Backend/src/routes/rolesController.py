from flask import Blueprint, request, jsonify, make_response
from src import app
from ..calls.rolesCalls import RolesCalls
from ..schemas.rolSchema import roles_schema,rol_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cors

@app.route('/roles', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def get_roles():
    respuesta = RolesCalls.get_roles()
    if respuesta is not None:
        return roles_schema.dump(respuesta)
    else:
        return jsonify(None)

@app.route('/roles/<int:id>', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def get_rol(id):
    respuesta = RolesCalls.get_rol_id(id)
    if respuesta is not None:
        return rol_schema.dump(respuesta)
    else:
        return jsonify(None)