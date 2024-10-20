from ..calls.asistenciasCalls import AsistenciasCalls
from ..calls.permisosCalls import PermisoCalls
from ..models.asistencia import Asistencia
from ..schemas.asistenciaSchema import asistencia_schema,asistencias_schema
from ..schemas.permisoSchema import permiso_schema,permisos_schema
from datetime import datetime, timedelta
import locale


class AsistenciasServices:
    def get_asistencias_empleado_mes(cedula, fecha):
        retorno = []

        asistencias = AsistenciasCalls.get_asistencias_empleado_mes(cedula, fecha)
        asistenciasJson = asistencias_schema.dump(asistencias)

        # Se buscan las fechas de la semana
        date = datetime.strptime(fecha, "%d/%m/%Y")
        inicioMes = datetime(date.year, date.month, 1)
        finMes = date.replace(day=28) + timedelta(days=4) 
        finMes = finMes - timedelta(days=finMes.day)

        # Se buscam los permisos
        permisos = PermisoCalls.get_permisos_empleado_fecha(cedula, fechaInicio=inicioMes.strftime('%d/%m/%Y'), fechaFin=finMes.strftime('%d/%m/%Y'))
        permisosJson = permisos_schema.dump(permisos)

        retorno = formatearAsistencias(asistenciasJson, permisosJson, inicioMes, finMes, False)
        return retorno
    
    def get_asistencias_permisos_reporte(turnos_empleados, fecha):
        for turno in turnos_empleados:
            for empleado in turno['trabajadores']:
                # Se buscam las asistencias
                asistencias = AsistenciasCalls.get_asistencias_empleado_semana(empleado['cedula'], fecha)
                asistenciasJson = asistencias_schema.dump(asistencias)

                # Se buscan las fechas de la semana
                date = datetime.strptime(fecha, "%d/%m/%Y")
                diaSemana = date.weekday()
                inicioSemana = date - timedelta(days=diaSemana)
                finSemana = inicioSemana + timedelta(days=6)

                # Se buscam los permisos
                permisos = PermisoCalls.get_permisos_empleado_fecha(empleado['cedula'], fechaInicio=inicioSemana.strftime('%d/%m/%Y'), fechaFin=finSemana.strftime('%d/%m/%Y'))
                permisosJson = permisos_schema.dump(permisos)

                semana = formatearAsistencias(asistenciasJson, permisosJson, inicioSemana, finSemana, True)
                empleado['semana'] = semana
        return turnos_empleados

    def get_asistencias_empleado_semana(cedula, fecha):
        asistencias = AsistenciasCalls.get_asistencias_empleado_semana(cedula, fecha)
        return asistencias_schema.dump(asistencias)
    
    def get_asistencias_empleado_dia(cedula, fecha):
        asistencia = AsistenciasCalls.get_asistencias_empleado_dia(cedula, fecha)
        return asistencia_schema.dump(asistencia)
    
    def registrar_entrada(json):
        asistencia = deserealizarJson(json)
        retorno = AsistenciasCalls.registrar_entrada(asistencia)
        if retorno is not None:
            return "00|OK"
        else:
            return "01|Problemas al registrar la asistencia"
    
    def registrar_salida(json):
        asistencia = deserealizarJson(json)
        retorno = AsistenciasCalls.registrar_salida(asistencia)
        if retorno is not None:
            return "00|OK"
        else:
            return "01|Problemas al registrar la asistencia"
        
# ----------------------------- FUNCIONES GENERALES ------------------------------
def formatearAsistencias(asistencias, permisos, fechaInicio, fechaFin, semana):
    retorno = []
    if semana == True:
        retorno = semanaBase()
    else:
        retorno = mesBase(fechaFin)
    # Se llenan los permisos
    retorno = llenarPermisos(permisos, fechaInicio, retorno)
    # Se llenan las asistencias
    if len(asistencias) > 0:
        for asistencia in asistencias:
            date = datetime.strptime(asistencia['hora_llegada'].split('T')[0], "%Y-%m-%d")
            if semana == True:
                # Obtener el día de la semana (0 para lunes, 6 para domingo)
                retorno[date.weekday()]['asistencia'] = True
            else:
                retorno[date.day - 1]['asistencia'] = True
    return retorno

def semanaBase():
    dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    retorno = []
    for i, dia in enumerate(dias):
        base = asistenciaBase()
        base['dia'] = dia
        base['numeroDia'] = i
        retorno.append(base)
    return retorno

def mesBase(fechaFin):
    configuracion_original = locale.getlocale()
    retorno = []
    fechaActual = fechaFin
    locale.setlocale(locale.LC_TIME, 'es_ES')
    for i in range(fechaFin.day):
        base = asistenciaBase()
        base['dia'] = fechaActual.strftime("%A").capitalize()
        base['numeroDia'] = fechaActual.day
        retorno.append(base)
        fechaActual = fechaActual - timedelta(days=1)
    locale.setlocale(locale.LC_TIME, configuracion_original)
    retorno.reverse()
    return retorno

def asistenciaBase():
    base = {
        'dia' : '',
        'asistencia' : None,
        'numeroDia' : -1
    }
    return base

def llenarPermisos(permisos, fechaInicio, retorno):
    if len(permisos) > 0:
        for permiso in permisos:
            fechaDia = fechaInicio
            inicioPermiso = datetime.strptime(permiso['fecha_inicio'].split('T')[0], "%Y-%m-%d")
            finPermiso = datetime.strptime(permiso['fecha_fin'].split('T')[0], "%Y-%m-%d")
            for dia in retorno:
                if finPermiso >= fechaDia >= inicioPermiso :
                    dia['asistencia'] = False
                fechaDia = fechaDia + timedelta(days=1)
    return retorno

def deserealizarJson(json):
    asistencia = Asistencia(comentario=json['comentario'], 
                      hora_llegada=json['hora_llegada'], 
                      hora_salida=json['hora_salida'],
                      empleado_cedula=int(json['empleado_cedula']))
    if 'id' in json:
        asistencia.id = int(json['id'])
    return asistencia