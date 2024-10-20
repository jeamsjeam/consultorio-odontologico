from ..calls.citasCalls import CitasCalls
from ..calls.pacienteCall import PacienteCalls
from ..calls.empleadosCalls import EmpleadosCalls
from ..models.cita import Cita
from datetime import datetime, timedelta
from ..schemas.citaSchema import cita_schema,citas_schema
from ..schemas.pacienteSchema import paciente_schema
from ..schemas.empleadoSchema import empleado_schema
from ..schemas.estadoCitaSchema import estado_cita_schema, estados_citas_schema
from ..services.generarPDFServices import GenerarPDF
from datetime import datetime
import tempfile
import base64
import pdb
import locale

class CitasServices:
    def agendar_cita(json):
        paciente = PacienteCalls.get_paciente_usuario(json['paciente_usuario'])

        if paciente is not None:
            paciente = paciente_schema.dump(paciente)
        else :
            return '03|Paciente no encontrado'
        
        cita = Cita(nota='', 
                      empleado_cedula=json['empleado_cedula'], 
                      paciente_cedula=paciente['cedula'],
                      fecha=json['fecha'],
                      estado_cita_id=1)
        
        citasMed = citas_schema.dump(CitasCalls.get_citas_dia_medico(cita.empleado_cedula, cita.fecha))
        citasPac = citas_schema.dump(CitasCalls.get_citas_dia_paciente(cita.paciente_cedula, cita.fecha))

        if len(citasPac) > 0:
            empleado = empleado_schema.dump(EmpleadosCalls.get_empleado_cedula(cita.empleado_cedula))
            for cita in citasPac:
                if cita['empleado']['especialidad']['nombre'] == empleado['especialidad']['nombre']:
                    return '03|Ya tienes una cita agendada para esta especialidad'

        if len(citasMed) < 8:
            cita.estado_cita_id = 1
            done = CitasCalls.crear_cita(cita)
            if done is not None:
                return '00|OK'
            else:
                return '01|Problemas al registrar cita'
        else:
            return '02|Este médico ha alcanzado su límite de pacientes para este día'
        
    def get_citas_paciente_mes(usuario, fecha):
        date = datetime.strptime(fecha, "%d/%m/%Y")
        finMes = date.replace(day=28) + timedelta(days=4) 
        finMes = finMes - timedelta(days=finMes.day)
        retorno = mesBase(finMes)

        paciente = PacienteCalls.get_paciente_usuario(usuario)
        if paciente is not None:
            paciente = paciente_schema.dump(paciente)
        else :
            return retorno
        
        citas = CitasCalls.get_citas_paciente_mes(paciente['cedula'], fecha)
        citasJson = citas_schema.dump(citas)

        # Se llenan las citas
        if len(citasJson) > 0:
            for cita in citasJson:
                date = datetime.strptime(cita['fecha'].split('T')[0], "%Y-%m-%d")
                retorno[date.day - 1]['estado'] = cita['estado_cita']['nombre']
                retorno[date.day - 1]['nota'] = cita['nota']
        return retorno
    
    def create_pdf_citas(persona, logo_path, titulo,tipo):
        # Crear instancia de PDF

        pdf = GenerarPDF(logo_path, titulo)
  
        pdf.add_page()

        # Llamar al método header para generar el encabezado
        #pdf.header()

        # Agregar imagen como logo (ajusta las coordenadas y dimensiones según tu necesidad)
        pdf.image(logo_path, 10, 8, 33)
        pdf.set_xy(0.0,0.0)
        pdf.set_font('Arial', 'B', 16)
        # self.set_text_color(76.0, 32.0 ,250.0)
        pdf.set_text_color(41, 0 ,199)
        pdf.cell(w=210.0, h=40.0, align='C', txt=titulo, border=0)
        pdf.set_text_color(0.0, 0.0 ,0.0)
        # Agregar cabeceras de columnas
        pdf.set_xy(10.0,50.0)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(35, 10, 'Cedula', 1, 0,'C')
        pdf.cell(35, 10, 'Nombre', 1, 0,'C')
        pdf.cell(35, 10, 'Apellido', 1, 0,'C')
        pdf.cell(35, 10, 'Telefono', 1, 0,'C')
        pdf.cell(35, 10, 'Cargo', 1, 0,'C')
        pdf.ln()
         
        pdf.set_font('Arial', '', 10)
        pdf.cell(35, 10, str(persona["cedula"]), 1, 0,'C')
        pdf.cell(35, 10, persona["nombre"], 1, 0,'C')
        pdf.cell(35, 10, persona["apellido"], 1, 0,'C')
        pdf.cell(35, 10, persona["telefono"], 1, 0,'C')
        pdf.cell(35, 10, persona["cargo"]["nombre"], 1, 0,'C')
        pdf.ln()
        #pdb.set_trace() 

        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(41, 0 ,199)
        pdf.cell(w=190.0, h=40.0, align='C', txt="Citas", border=0)
        pdf.set_text_color(0.0, 0.0 ,0.0)
        # Agregar cabeceras de columnas
        pdf.set_xy(10.0,100.0)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(45, 10, 'Fecha', 1, 0,'C')
        if tipo == 2:
            pdf.cell(45, 10, 'Paciente', 1, 0,'C')
        else:
            pdf.cell(45, 10, 'Medico', 1, 0,'C')
        pdf.cell(45, 10, 'Nota', 1, 0,'C')
        pdf.cell(45, 10, 'Estado', 1, 0,'C')
        pdf.ln()

        # Agregar datos de pacientes al PDF
        for cita in persona["citas"]:
            pdf.set_font('Arial', '', 10)
            pdf.cell(45, 10, str(cita["fecha"].split("T")[0]), 1, 0,'C')
            if tipo  == 2:
                pdf.cell(45, 10, cita["paciente"]["nombre"] + " " + cita["paciente"]["apellido"], 1, 0,'C')
            else:
                pdf.cell(45, 10, cita["empleado"]["nombre"] + " " + cita["empleado"]["apellido"], 1, 0,'C')
            pdf.cell(45, 10, cita["nota"], 1, 0,'C')
            pdf.cell(45, 10, cita["estado_cita"]["nombre"], 1, 0,'C')
            pdf.ln()

        # Llamar al método footer para generar el pie de página
        pdf.footer()
        
        # Crear un archivo temporal para guardar el PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            pdf_path = temp_file.name
            pdf.output(pdf_path)

        return pdf_path
    
    

def deserealizarJson(json):
    cita = Cita(nota=json['nota'], 
                      empleado_cedula=json['empleado_cedula'], 
                      paciente_cedula=json['paciente_cedula'],
                      fecha=json['fecha'],
                      estado_cita_id=int(json['estado_cita_id']))
    if 'id' in json:
        cita.id = int(json['id'])
    return cita

def mesBase(fechaFin):
    configuracion_original = locale.getlocale()
    retorno = []
    fechaActual = fechaFin
    locale.setlocale(locale.LC_TIME, 'es_ES')
    for i in range(fechaFin.day):
        base = citaBase()
        base['numeroDia'] = fechaActual.day
        retorno.append(base)
        fechaActual = fechaActual - timedelta(days=1)
    locale.setlocale(locale.LC_TIME, configuracion_original)
    retorno.reverse()
    return retorno


def citaBase():
    base = {
        'nota' : '',
        'estado' : None,
        'numeroDia' : -1
    }
    return base
    
