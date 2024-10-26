from ..calls.usuarioCalls import UsuarioCalls
from ..models.usuario import Usuario

class UsuarioServices:
    def ObtenerUsuarios():
        return UsuarioCalls.ObtenerUsuarios()

    def AutenticarUsuario(datos):
        return UsuarioCalls.AutenticarUsuario(datos)
    
    def CrearUsuario(datos):
        return UsuarioCalls.CrearUsuario(datos)
