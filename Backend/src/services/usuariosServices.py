from ..calls.usuariosCalls import UsuariosCalls
from ..calls.rolesCalls import RolesCalls
from ..models.usuario import Usuario

class UsuariosServices:

    def usuario_rol_por_nombre(usuario):
        usuario = UsuariosCalls.usuario_por_nombre(usuario)
        if usuario is not None:
            rol = RolesCalls.get_rol_id(usuario.rol_id)
            return rol
        else:
            return None
        
    def usuario_por_nombre(usuario):
        usuario = UsuariosCalls.usuario_por_nombre(usuario)
        if usuario is not None:
            return usuario
        else:
            return None

    def login(usuario, clave):
        return UsuariosCalls.autenticar_usuario(usuario, clave)
    
    def register(json):
        respuesta = ''
        if es_admin(json['usuarioValidador'], json['claveValidador']):
            existeUsuario = UsuariosCalls.usuario_por_nombre(json['usuario'])
            if existeUsuario is None:
                usuarioNuevo = Usuario(usuario=json['usuario'], clave=json['clave'], nombre=json['nombre'], rol_id=json['rol_id'])
                done = UsuariosCalls.crear_usuario(usuarioNuevo)
                if done is None:
                    respuesta = '01|Problemas al crear usuario'
                else :
                    #respuesta = '00|' + done.nombre
                    respuesta = '00|Usuario Creado Con Exito'
            else:
                respuesta = '03|Usuario ya existe'
        else :
            respuesta = '01|Problemas con el usuario validador'
        return respuesta

def es_admin(usuario, clave):
    validadorLogin = UsuariosCalls.autenticar_usuario(usuario, clave)
    if validadorLogin == '00|OK':
        validador = UsuariosCalls.usuario_por_nombre(usuario)
        if RolesCalls.permite_crear(validador.rol_id):
            return True
    return False


        