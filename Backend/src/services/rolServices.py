from ..calls.rolesCalls import RolesCalls
from ..models.rol import Rol

class RolServices:
    def ObtenerRoles():
        return RolesCalls.ObtenerRoles()
    
    def PermiteCrear(id):
        rol = RolesCalls.ObtenerRolPorId(id)
        if rol.nombre.upper().find('ADMINISTRADOR') != -1:
            return True
        else:
            return False
    
    def ObtenerRolPorId(id):
        return RolesCalls.ObtenerRolPorId(id)
    
    def ObtenerRolPorNombre(nombre):
        return RolesCalls.ObtenerRolPorNombre(nombre)