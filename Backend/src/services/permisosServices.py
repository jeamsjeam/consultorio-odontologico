from ..calls.permisosCalls import PermisoCalls
from ..models.permiso import Permiso
from ..schemas.permisoSchema import permiso_schema,permisos_schema
from datetime import datetime

class PermisosServices:
    def registrarPermiso(json):
        permiso = deserealizarJson(json)
        dateInicio = datetime.strptime(permiso.fecha_inicio, "%d/%m/%Y")
        dateFin = datetime.strptime(permiso.fecha_fin, "%d/%m/%Y")
        if dateFin  >= dateInicio :
            anteriores = permisos_schema.dump(PermisoCalls.get_permisos_empleado_fecha(permiso.empleado_cedula, permiso.fecha_inicio, permiso.fecha_fin))
            if len(anteriores) == 0:
                done = PermisoCalls.registrar_permiso(permiso)
                if done is not None:
                    return '00|OK'
                else:
                    return '01|Problemas al registrar el permiso'
            else:
                return '02|Este empleado ya tiene un permiso activo para esta fecha'
        else:
            return '03|Las fecha de inicio no puede ser mayor a la fecha final'
        
    def consultarPermisosEmpleado(cedula):
        permisos = PermisoCalls.get_permisos_empleado(cedula)
        return permisos_schema.dump(permisos) 
    
    def get_permisos_cedula_fecha(cedula, fechaInicio, fechaFin):
        permisos = PermisoCalls.get_permisos_empleado_fecha(cedula, fechaInicio, fechaFin)
        return permisos_schema.dump(permisos) 

def deserealizarJson(json):
    permiso = Permiso(descripcion_motivo= json['descripcion_motivo'],
                        fecha_inicio= json['fecha_inicio'],
                        fecha_fin= json['fecha_fin'],
                        empleado_cedula= int(json['empleado_cedula']))
    return permiso