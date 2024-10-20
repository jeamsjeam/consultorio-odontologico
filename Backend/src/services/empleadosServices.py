from ..calls.empleadosCalls import EmpleadosCalls
from ..calls.citasCalls import CitasCalls
from ..models.empleado import Empleado
from ..schemas.empleadoSchema import empleado_schema,empleados_schema
from ..schemas.citaSchema import cita_schema,citas_schema
from ..schemas.estadoEmpleadoSchema import estados_empleados_schema, estado_empleado_schema

class EmpleadosServices:
    def get():
        empleados = EmpleadosCalls.get_empleados()
        return empleados_schema.dump(empleados)
    
    def buscar(cedula):
        empleado = EmpleadosCalls.get_empleado_cedula(cedula)
        return empleado_schema.dump(empleado)

    def entrada(empleado_cedula, fecha):
        respuesta = ''
        return respuesta

    def guardar(json):
        empleado = deserealizarJson(json)
        repetido = EmpleadosCalls.get_empleado_cedula(empleado.cedula)
        if repetido is None:
            done = EmpleadosCalls.crear_empleado(empleado)
            if done is not None:
                return '00|OK'
            else:
                return '01|Problemas al registrar empleado'
        else:
            done = EmpleadosCalls.modificar_empleado(empleado)
            if done is not None:
                return '00|OK'
            else:
                return '01|Problemas al registrar empleado'

    def borrar(id):
        return EmpleadosCalls.borrar_empleado(id)
    
    def get_empleados_especialidad():
        return agruparEmpleados('especialidad')
    
    def get_empleados_turno():
        return agruparEmpleados('turno')
    
    def get_medicos_especialidad(especialidad_id):
        medicos = EmpleadosCalls.get_medicos_especialidad(especialidad_id)
        medicosJson = empleados_schema.dump(medicos)
        retorno = []
        if len(medicosJson) > 0:
            for medico in medicosJson:
                agregar = infoBasica(medico)
                retorno.append(agregar)
        return retorno
    
    def buscar_citas(cedula):

        # Se busca al paciente
        empleadoConsulta = EmpleadosCalls.get_empleado_cedula(cedula)
        
        # Si existe el paciente se procede a buscar sus reposos
        if empleadoConsulta is not None:

            # Se convierte el objeto Paciente a un diccionario
            empleado = empleado_schema.dump(empleadoConsulta)   
            #pdb.set_trace()  

            if empleado["cargo"]["nombre"] != "Medico":
                return None

            # SSe consultan las citas
            consultaCitas = CitasCalls.get_citas_medico(empleado['cedula'])

            # Se verifica que exista citas
            if consultaCitas is not None and len(consultaCitas) > 0:

                # Se convierte el objeto citas en un diccionario
                citas = citas_schema.dump(consultaCitas)

                # Se agregan las citas
                empleado['citas'] = citas
                return empleado

            else:
                # Se envia las citas vacias
                empleado['citas'] = []
                return empleado
        else:
            # Si no se encuentra paciente se retorna null
            return None
        
    
def agruparEmpleados(filtro):
    empleadosConsulta = EmpleadosCalls.get_empleados()
    empleados = empleados_schema.dump(empleadosConsulta)
    retorno = []
    if len(empleados) > 0:
        for empleado in empleados:
            if any(especialidad[filtro] == empleado[filtro]['nombre'] for especialidad in retorno):
                for item in retorno:
                    if item[filtro] == empleado[filtro]['nombre']:
                        agregar = infoBasica(empleado)
                        item['trabajadores'].append(agregar)
            else :
                nuevo = { filtro : empleado[filtro]['nombre'], 'trabajadores' : []}
                agregar = infoBasica(empleado)
                nuevo['trabajadores'].append(agregar)
                retorno.append(nuevo)
        return retorno
    return []

def deserealizarJson(json):
    empleado = Empleado(cedula= int(json['cedula']),
                            nombre= json['nombre'],
                            apellido= json['apellido'],
                            fecha_nacimiento= json['fecha_nacimiento'],
                            direccion= json['direccion'],
                            telefono= json['telefono'],
                            especialidad_id= int(json['especialidades']),
                            cargo_id= int(json['cargos']),
                            dependencia_id= int(json['dependencias']),
                            turno_id= int(json['turnos']),
                            genero_id= int(json['generos']),
                            estado_empleado_id= int(json['estados_empleados']))
    return empleado

def infoBasica(empleado):
    info = {
        'cedula' : empleado['cedula'],
        'nombre' :  empleado['nombre'] + " " +  empleado['apellido'],
        'cargo' :  empleado['cargo']['nombre']
    }
    return info
    