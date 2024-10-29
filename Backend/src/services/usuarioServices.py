from ..calls.usuarioCalls import UsuarioCalls

class UsuarioServices:
    def ObtenerUsuarios():
        return UsuarioCalls.ObtenerUsuarios()

    def AutenticarUsuario(datos):
        return UsuarioCalls.AutenticarUsuario(datos)
    
    def CrearUsuario(datos):
        try:
            existe = UsuarioCalls.ObtenerUsuarioPorUsuario(datos.usuario)
            if existe is not None:
                    raise Exception(f"Usuario registrado")
                
            return UsuarioCalls.CrearUsuario(datos)
        except Exception as e:
                print(f"Error al insertar usuario: {e}")
                raise Exception(f"Error al insertar usuario: {e}")
    
    
