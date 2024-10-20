from ..calls.turnosCalls import TurnosCalls
from ..models.turno import Turno

class TurnosServices:
    def get():
        return TurnosCalls.get_turnos()
    
    def buscar(id):
        return TurnosCalls.get_turno_id(id)
    
    def crear(json):
        turno = deserealizarJson(json)
        repetido = TurnosCalls.get_turno_nombre(turno.nombre)
        if repetido is None:
            done = TurnosCalls.crear_turno(turno)
            if done is not None:
                return '00|OK'
            else:
                return '01|Problemas al registrar turno'
        else:
            return '02|Turno repetido'
        
    def modificar(json):
        turno = deserealizarJson(json)
        return TurnosCalls.modificar_turno(turno)

    def borrar(id):
        turnoBD = TurnosCalls.get_turno_id(id)
        if len(turnoBD.empleados) > 0:
            return "01|No se puede borrar el turno ya que tiene trabajadores asociados"
        return TurnosCalls.borrar_turno(id)
    
    def guardarTurnos(listaTurnos):
        for turnoJson in listaTurnos:
            if turnoJson['id'] == 0:
                TurnosServices.crear(turnoJson)
            else :
                TurnosServices.modificar(turnoJson)
        return "00|OK"

def deserealizarJson(json):
    turno = Turno(nombre=json['nombre'], 
                      hora_llegada=json['hora_llegada'], 
                      hora_salida=json['hora_salida'])
    if 'id' in json:
        turno.id = int(json['id'])
    return turno