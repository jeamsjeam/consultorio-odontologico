from ..calls.rolCalls import RolCalls

class RolServices:
    def ObtenerRoles():
        return RolCalls.ObtenerRoles()

    def ObtenerRolPorId(id):
        return RolCalls.ObtenerRolPorId(id)
    
    def PermiteCrear(id):
        rol = RolCalls.ObtenerRolPorId(id)
        if rol.nombre.upper().find('ADMINISTRADOR') != -1:
            return True
        else:
            return False
    
    def ObtenerRolPorNombre(nombre):
        return RolCalls.ObtenerRolPorNombre(nombre)