from ..models.rol import Rol

class RolesCalls():

    def ObtenerRoles():
        return sorted(Rol.query.all(), key=lambda x: x.nombre)

    def ObtenerRolPorId(id):
        return Rol.query.get(id)
    
    def ObtenerRolPorNombre(nombre):
        return Rol.query.filter_by(nombre=nombre).first()

