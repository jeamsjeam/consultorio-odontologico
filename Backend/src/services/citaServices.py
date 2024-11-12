from ..calls.citaCalls import CitaCalls
from ..calls.fechaCalls import FechaCalls
from ..calls.personaCalls import PersonaCalls
from ..calls.servicioCalls import ServicioCalls
from ..calls.servicioCalls import ServicioCalls
from ..models.fecha import Fecha
from ..models.cita import Cita
from datetime import datetime

class CitasServices:
    def ObtenerCitas():
        return CitaCalls.ObtenerCitas()
    
    def ObtenerCitaPorFecha(datos):
        try:
            
            existeFecha = FechaCalls.ObtenerFechaPorFecha(datos.fecha)

            if existeFecha is None:
                raise Exception(f"No se encontro la fecha ingresada")
            
            return CitaCalls.ObtenerCitasPorFechaId(existeFecha.id)
            
        except Exception as e:
            print(f"Error al obtener cita: {e}")
            raise Exception(f"Error al obtener cita: {e}")
        
    def ObtenerPorCedula(cedula):
        try:
            
            existePerosna = PersonaCalls.ObtenerPersonaPorCedula(cedula)

            if existePerosna is None:
                raise Exception(f"No se encontro la cedula")
            
            return CitaCalls.ObtenerCitasPorPersonaId(existePerosna.id)
            
        except Exception as e:
            print(f"Error al obtener cita: {e}")
            raise Exception(f"Error al obtener cita: {e}")
        
    def CrearCita(datos):
        try:

            # se verifica que la fecha enviada no sea menor a la actual
            if datetime.strptime(datos.fecha, "%Y-%m-%d") < datetime.now():
                # mostrar mensaje de error por fecha menor a la actual
                raise Exception(f"Fecha ingresada menor a la fecha actual")
            
            # se obtiene persona por cedula 
            persona = PersonaCalls.ObtenerPersonaPorCedula(datos.cedula)
            # si persona es none 
            if persona is None:
                # mostrar mensaje de persona no encontrada 
                raise Exception(f"Persona no encontrada")
            
            # obtener detalles de un servicio por id 
            servicio = ServicioCalls.ObtenerServicioPorId(datos.servicioId)
            # si el servicio es none
            if servicio is None:
               # 
                raise Exception(f"Servicio no encontrada")

            # Variable que guarda el id de la fecha que se va a registar en la cita
            fechaId = 0

            # obtener fecha por fecha 
            existeFecha = FechaCalls.ObtenerFechaPorFecha(datos.fecha)

             # si la fecha es none 
            if existeFecha is None:
                # se crea nueva fecha utilizando crearfecha de la clase fechacalls
                nuevafecha = FechaCalls.CrearFecha(Fecha(fecha = datos.fecha, cantidad=3))

                # se guarda el nuevo id de la fecha 
                fechaId = nuevafecha.id

            #sino la fecha no es none 
            else:
                # Obtener las citas asociadas a la fecha con el identificador 'id' del objeto 'existeFecha'
                citasFecha = CitaCalls.ObtenerCitasPorFechaId(existeFecha.id)

                # verifica la cantidad de las cita programada es mayor o igual al limite permitido por citas 
                # if len (citasFecha) se obtiene la cantidad de citas programadas 
                # existeFecha. cantidad , esta variable se encarga del limite permitido por citas de la fecha 
                if len(citasFecha) >= existeFecha.cantidad:
                    raise Exception(f"Cantidad citas por fecha superada")
                
                # se agraga valor a fechaid con una nueva fecha 
                fechaId = existeFecha.id
                 # obtener citas por persona y fecha 
                 # se utiliza para obtener una lista de citas de una persona específica en una fecha dada por el id 
                existeCitaPersonaFecha = CitaCalls.ObtenerCitasPorPersonaYFecha(persona.id, fechaId)

                #verificar que la persona ya tiene una cita 
                if existeCitaPersonaFecha is not None:
                    raise Exception(f"Persona ya tiene una cita para esa fecha")
                
            # Crear  una nueva cita 
            # personaid=persona.id  es el id de la persona que realiza la solicitud para la cita 
            # servicioid=servicioid  es el id del servicio que se desea reservar 
            # estadocitaid=1  es el estado de la cita 
            # fechaid=fechaid es la fecha de la cita 
            nuevaCita = Cita(personaId=persona.id, 
                             servicioId=servicio.id,
                             estadoCitaId=1,
                             fechaId=fechaId)

            return CitaCalls.CrearCita(nuevaCita)
        except Exception as e:
            print(f"Error al insertar cita: {e}")
            raise Exception(f"Error al insertar cita: {e}")
        
    def ActualizarCita(datos):
        try:
            # Validar que el id esté presente, no sea None y sea positivo
            if not hasattr(datos, 'id') or datos.id is None or datos.id < 0:
                raise Exception("ID del cita no proporcionado o inválido")

            # Comprobar que la cita exista en la base de datos
            consulta = CitaCalls.ObtenerCitaPorId(datos.id)
            if not consulta:
                raise Exception("cita no encontrado")
            
            # Recorrer todos los atributos de 'datos' y asignarlos si existen en consulta, excluyendo 'id'
            for key, value in datos.__dict__.items():
                if key != 'id' and hasattr(consulta, key) and value is not None:
                    setattr(consulta, key, value)

            # Llamar a la función de actualización si la validación es exitosa
            return CitaCalls.ActualizarCita(consulta)
        except Exception as e:
            print(f"Error al actualizar cita: {e}")
            raise Exception(f"Error al actualizar cita: {e}")




    
