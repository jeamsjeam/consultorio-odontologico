from flask import Blueprint, request, jsonify, make_response
from ..viewModels.customJsonify import CustomJsonify
from src import app
from types import SimpleNamespace
from ..services.usuarioServices import UsuarioServices
from ..schemas.usuarioSchema import usuario_schema,usuarios_schema
from flask_cors import cross_origin # Se utiliza para evitar el problema de cors
import json


@app.route('/usuario', methods=['GET'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def ObtenerUsuarios():
    respuesta = UsuarioServices.ObtenerUsuarios()
    return CustomJsonify(respuesta, usuario_schema, usuarios_schema)
    
@app.route('/usuario/AutenticarUsuario', methods=['POST'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def AutenticarUsuario():
    respuesta = UsuarioServices.AutenticarUsuario(json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d)))
    return CustomJsonify(respuesta, usuario_schema, usuarios_schema)

@app.route('/usuario/CrearUsuario', methods=['POST'])
@cross_origin() # Se debe colocar en servicio para evitar problemas de cors
def CrearUsuario():
    respuesta = UsuarioServices.CrearUsuario(json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d)))
    return CustomJsonify(respuesta, usuario_schema, usuarios_schema)