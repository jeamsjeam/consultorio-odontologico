from ..calls.usuarioCalls import UsuarioCalls
from ..models.usuario import Usuario

class UsuarioServices:
    def ObtenerUsuarios():
        return UsuarioCalls.ObtenerUsuarios()

    def AutenticarUsuario(datos):
        return UsuarioCalls.AutenticarUsuario(datos)
    
    def CrearUsuario(datos):
        try:
            # Se verifica si existe un registro con la misma cedula
            existe = UsuarioCalls.ObtenerUsuarioPorUsuario(datos.usuario)
            if existe is not None:
                raise Exception(f"Usuario registrado")
                
             # Filtrar solo los atributos válidos para el modelo usuario
            atributosValidos = {key: value for key, value in datos.__dict__.items() if hasattr(Usuario, key) and value is not None}

            # Crear una instancia de usuario con los atributos filtrados
            nuevo = Usuario(**atributosValidos)

            return UsuarioCalls.CrearUsuario(nuevo)
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            raise Exception(f"Error al insertar usuario: {e}")
        
    def ActualizarUsuario(datos):
        try:
            # Validar que el id esté presente, no sea None y sea positivo
            if not hasattr(datos, 'id') or datos.id is None or datos.id < 0:
                raise Exception("ID del usuario no proporcionado o inválido")

            # Comprobar que la usuario exista en la base de datos
            consulta = UsuarioCalls.ObtenerUsuarioPorId(datos.id)
            if not consulta:
                raise Exception("usuario no encontrado")
            
            # Recorrer todos los atributos de 'datos' y asignarlos si existen en consulta, excluyendo 'id'
            for key, value in datos.__dict__.items():
                if key != 'id' and hasattr(consulta, key) and value is not None:
                    setattr(consulta, key, value)

            # Llamar a la función de actualización si la validación es exitosa
            return UsuarioCalls.ActualizarUsuario(consulta)
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            raise Exception(f"Error al actualizar usuario: {e}")
    
    
