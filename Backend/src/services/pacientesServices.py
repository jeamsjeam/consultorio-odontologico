from ..calls.pacienteCall import PacienteCalls
from ..calls.grupoRepososCalls import GrupoReposoCalls
from ..calls.repososCalls import ReposoCalls
from ..calls.cargosCalls import CargosCalls
from ..calls.usuariosCalls import UsuariosCalls
from ..calls.dependenciasCalls import DependenciasCalls
from ..calls.municipiosCalls import MunicipiosCalls
from ..calls.tipoReposoCall import TipoReposoCalls
from ..calls.rolesCalls import RolesCalls
from ..calls.citasCalls import CitasCalls
from ..calls.citasCalls import CitasCalls
from ..models.paciente import Paciente
from ..models.grupo_reposo import GrupoReposo
from ..models.reposo import Reposo
from ..models.usuario import Usuario
from ..schemas.pacienteSchema import paciente_schema,Pacientes_schema
from ..schemas.grupoReposoSchema import grupoReposo_schema,grupoReposos_schema
from ..schemas.reposoSchema import reposo_schema,reposos_schema
from ..schemas.cargoSchema import cargo_schema,cargos_schema
from ..schemas.dependenciaSchema import dependecia_schema,dependecias_schema
from ..schemas.municipioSchema import municipio_schema,municipios_schema
from ..schemas.citaSchema import cita_schema,citas_schema
from ..services.generarPDFServices import GenerarPDF
from datetime import datetime
import tempfile
import base64
import pdb

class PacientesServices:

    def buscarTodos():
        # Se busca al paciente
        pacientes = PacienteCalls.get_paciente()

        if pacientes is None or len(pacientes) < 1:
            return None

        listaPacientes = []

        for pacienteConsulta in pacientes:
            # Guarda la cantidad de dias de los reposos
            total_dias_reposos = 0

            # Si existe el paciente se procede a buscar sus reposos
            if pacienteConsulta is not None:

                # Se convierte el objeto Paciente a un diccionario
                paciente = paciente_schema.dump(pacienteConsulta)   
                #pdb.set_trace()  

                # Se buscan los grupos de reposos de ese paciente y se retornan en orden de la fecha mas actual a la mas antigua
                grupoReposoConsulta = GrupoReposoCalls.get_grupoReposo_paciente(paciente['cedula'])

                # Se verifica que exista al menos un grupo de reposo
                if grupoReposoConsulta is not None and len(grupoReposoConsulta) > 0:

                    # Se convierte el objeto GrupoReposo en un diccionario
                    grupoReposo = grupoReposos_schema.dump(grupoReposoConsulta)

                    # Se crea una lista donde se van a guardar los reposos del paciente
                    #listaReposos = []
                    
                    # Se utiliza para poder saber cual es el primer grupo reposo para sumar solo esos dias
                    #banderaDias = True

                    # Se recorren todos los grupos de reposos encontrados
                    for grupo in grupoReposo:

                        # Se buscan los reposos de cada grupo de reposos y se traen en orden de la fecha mas actual a la mas antigua
                        reposoConsulta = ReposoCalls.get_reposo_paciente(grupo['id'])

                        # Se verifica que existan reposos
                        if reposoConsulta is not None and len(reposoConsulta) > 0:

                            # Se recorren todos los reposos y se agregan a la lista 
                            for rep in reposoConsulta:

                                # Se suman los dias del grupo reposo mas nuevo
                                #if banderaDias:
                                total_dias_reposos += (rep.fecha_fin - rep.fecha_inicio).days + 1

                                #listaReposos.append(rep)

                        # se cambia la bandera de estado para que ya no cuente mas dias
                        # banderaDias = False
                        break
                    
                    # Si se agrego algo a lista se agrega al objeto paciente un nuevo campo llamado reposo donde estara la lista que se acabo de llenar
                    # En caso de que no exista nada en la lista se agrega vacia
                    # if listaReposos is not None and len(listaReposos) > 0:

                    #     # Se convierte el objeto Reposos en un diccionario y se agrega al objeto paciente
                    #     #paciente['reposos'] = reposos_schema.dump(listaReposos)
                    #     paciente["dias_reposo"] = total_dias_reposos
                    # else:
                    #     #paciente['reposos'] = []
                    #     paciente["dias_reposo"] = total_dias_reposos
                    paciente["dias_reposo"] = total_dias_reposos
                    listaPacientes.append(paciente)
                else:
                    # Si el paciente no se le encontraron grupo de reposos se envia la lista de reposos vacia 
                    #paciente['reposos'] = []
                    paciente["dias_reposo"] = total_dias_reposos
                    listaPacientes.append(paciente)
        return listaPacientes

    def buscar(cedula):

        # Se busca al paciente
        pacienteConsulta = PacienteCalls.get_paciente_cedula(cedula)

        # Guarda la cantidad de dias de los reposos
        total_dias_reposos = 0

        # Si existe el paciente se procede a buscar sus reposos
        if pacienteConsulta is not None:

            # Se convierte el objeto Paciente a un diccionario
            paciente = paciente_schema.dump(pacienteConsulta)   
            #pdb.set_trace()  

            # Se buscan los grupos de reposos de ese paciente y se retornan en orden de la fecha mas actual a la mas antigua
            grupoReposoConsulta = GrupoReposoCalls.get_grupoReposo_paciente(paciente['cedula'])

            # Se verifica que exista al menos un grupo de reposo
            if grupoReposoConsulta is not None and len(grupoReposoConsulta) > 0:

                # Se convierte el objeto GrupoReposo en un diccionario
                grupoReposo = grupoReposos_schema.dump(grupoReposoConsulta)

                # Se crea una lista donde se van a guardar los reposos del paciente
                listaReposos = []
                
                # Se utiliza para poder saber cual es el primer grupo reposo para sumar solo esos dias
                banderaDias = True
                # Se recorren todos los grupos de reposos encontrados
                for grupo in grupoReposo:

                    # Se buscan los reposos de cada grupo de reposos y se traen en orden de la fecha mas actual a la mas antigua
                    reposoConsulta = ReposoCalls.get_reposo_paciente(grupo['id'])

                    # Se verifica que existan reposos
                    if reposoConsulta is not None and len(reposoConsulta) > 0:

                        # Se recorren todos los reposos y se agregan a la lista 
                        for rep in reposoConsulta:

                            # Se suman los dias del grupo reposo mas nuevo
                            if banderaDias:
                                total_dias_reposos += (rep.fecha_fin - rep.fecha_inicio).days + 1

                            listaReposos.append(rep)

                    # se cambia la bandera de estado para que ya no cuente mas dias
                    banderaDias = False
                
                # Si se agrego algo a lista se agrega al objeto paciente un nuevo campo llamado reposo donde estara la lista que se acabo de llenar
                # En caso de que no exista nada en la lista se agrega vacia
                if listaReposos is not None and len(listaReposos) > 0:

                    # Se convierte el objeto Reposos en un diccionario y se agrega al objeto paciente
                    paciente['reposos'] = reposos_schema.dump(listaReposos)
                    paciente["dias_reposo"] = total_dias_reposos
                else:
                    paciente['reposos'] = []
                    paciente["dias_reposo"] = total_dias_reposos
                return paciente
            else:
                # Si el paciente no se le encontraron grupo de reposos se envia la lista de reposos vacia 
                paciente['reposos'] = []
                paciente["dias_reposo"] = total_dias_reposos
                return paciente
        else:
            # Si no se encuentra paciente se retorna null
            return None
    
    def buscar_citas(cedula):

        # Se busca al paciente
        pacienteConsulta = PacienteCalls.get_paciente_cedula(cedula)

        # Si existe el paciente se procede a buscar sus reposos
        if pacienteConsulta is not None:

            # Se convierte el objeto Paciente a un diccionario
            paciente = paciente_schema.dump(pacienteConsulta)   
            #pdb.set_trace()  

            # SSe consultan las citas
            consultaCitas = CitasCalls.get_citas_paciente(paciente['cedula'])

            # Se verifica que exista citas
            if consultaCitas is not None and len(consultaCitas) > 0:

                # Se convierte el objeto citas en un diccionario
                citas = citas_schema.dump(consultaCitas)

                # Se agregan las citas
                paciente['citas'] = citas
                return paciente

            else:
                # Se envia las citas vacias
                paciente['citas'] = []
                return paciente
        else:
            # Si no se encuentra paciente se retorna null
            return None
        
    def eliminar_paciente(cedula):

        # Se busca al paciente
        pacienteConsulta = PacienteCalls.get_paciente_cedula(cedula)
        #pdb.set_trace() 

        # Si existe el paciente se procede a buscar sus reposos
        if pacienteConsulta is not None:
 
            # Se buscan los grupos de reposos de ese paciente y se retornan en orden de la fecha mas actual a la mas antigua
            grupoReposoConsulta = GrupoReposoCalls.get_grupoReposo_paciente(pacienteConsulta.cedula)

            # Se verifica que exista al menos un grupo de reposo
            if grupoReposoConsulta is not None and len(grupoReposoConsulta) > 0:

                # Se recorren todos los grupos de reposos encontrados
                for grupo in grupoReposoConsulta:

                    # Se buscan los reposos de cada grupo de reposos y se traen en orden de la fecha mas actual a la mas antigua
                    reposoConsulta = ReposoCalls.get_reposo_paciente(grupo.id)

                    # Se verifica que existan reposos
                    if reposoConsulta is not None and len(reposoConsulta) > 0:

                        # Se recorren todos los reposos y se agregan a la lista 
                        for rep in reposoConsulta:
                            borradoReposo = ReposoCalls.borrar_reposo_sin_consultar(rep)  

                    borradoGrupoReposo = GrupoReposoCalls.borrar_grupoReposo_sin_consultar(grupo)
            
            # Se consulta las citas para borrarlo
            citas = CitasCalls.get_citas_paciente(pacienteConsulta.cedula)
            if citas is not None and len(citas) > 0:
                for cita in citas:
                    borradoCitas = CitasCalls.borrar_ucita_sin_consultar(cita)
                    
            borradoPaciente = PacienteCalls.borrar_paciente_sin_consultar(pacienteConsulta)

            # Se consulta el usuario para borrarlo
            usuario = UsuariosCalls.usuario_por_nombre(pacienteConsulta.cedula)

            if usuario is not None:
                borradoUsuario = UsuariosCalls.borrar_usuario_sin_consultar(usuario)

            if borradoPaciente == True:
                return "00|Borrado exitoso"
            else:
                return "02|Error al borrar"
        else:
            return "01|No se encontro paciente"
    
    def crear_paciente(datos_completos):

        # Se crea un diccionario de salida
        resultadoDiccionario = {}

        # Se busca el rol Paciente
        rol = RolesCalls.get_rol_nombre("Paciente")

        # Id del usuario
        idUsuario = 0

        # Se consulta si ya existe un usuario con ese usuario especifico
        existeUsuario = UsuariosCalls.usuario_por_nombre(str(datos_completos["cedula"]))

        # Si existe se guarda su id si no se crea uno nuevo
        if existeUsuario is not None:
            idUsuario = existeUsuario.id
        else:
            # Se crea un diccionario que contendra la informacion del nuevo usuario
            usuario_diccionario = {
                "usuario": str(datos_completos["cedula"]),
                "clave": datos_completos["cedula"],
                "nombre": datos_completos["nombre"],
                "rol_id": rol.id
            }
            #pdb.set_trace()
            # Se convierte en objeto el diccionario
            usuario = UsuariosCalls.crear_obj_usuario(usuario_diccionario)

            # Se crea el usuario
            usuarioNuevo = UsuariosCalls.crear_usuario(usuario)

            # Si no se pudo crear el usuario se retorna un error 
            if usuarioNuevo is None:
                resultadoDiccionario["mensaje"] = "02|No se pudo crear usuario"
                resultadoDiccionario["paciente"] = None
                return resultadoDiccionario
            idUsuario = usuarioNuevo.id


        # Se agrega un campo nuevo al objeto que tiene los datos del paciente con el usuario id
        datos_completos["usuario_id"] = idUsuario

        # Creamos el objeto paciente con los datos recibidos
        paciente = PacienteCalls.crear_obj_paciente(datos_completos)

        # Se cre ale paciente 
        paciente_creado = PacienteCalls.crear_paciente(paciente)

        # Se verifica si la creacion del paciente se hizo con existo
        # Si fue exitosa se retona un mensaje y el objeto paciente agregandole un campo mas de reposos que es una lista vacia
        # Si no se pudo crear se retorna un mensaje de error y el objeto paciente null
        if paciente_creado is not None:
            resultadoDiccionario["mensaje"] = "00|Paciente Registrados con exito"
            resultado = paciente_schema.dump(paciente_creado)
            resultado["dias_reposo"] = 0
            resultado["reposos"] = []
            resultadoDiccionario["paciente"] = resultado
            return resultadoDiccionario
        else:
            resultadoDiccionario["mensaje"] = "01|Error al registrar el paciente"
            resultadoDiccionario["paciente"] = None
            return resultadoDiccionario
    
    def registrar_reposo(datos_completos):

        # Se busca al paciente
        pacienteConsulta = PacienteCalls.get_paciente_cedula(datos_completos['cedula'])

        # Si no se encuentra se retorna el mensaje
        if pacienteConsulta is None:
            return "02|No se encontro paciente"
        
        # Creamos el objeto grupo_reposo con los datos recibidos
        grupo_reposo = GrupoReposoCalls.retornar_obj_grupoReposo(datos_completos)

        # Se consulta el servicio que trae el ultimo grupoReposo y sus reposos
        # Si no han pasado mas de 180 dias desde la fecha inicio del grupo hasta la fecha inicio del reporte nuevo
        resultado = GrupoReposoCalls.buscar_grupoReposo(datos_completos['cedula'], datos_completos['grupo_reposo_fecha_inicio'])

        # Se pregunta si el resultado es un string, de ser asi quiere decir que o no tiene o los dias son mayores a 180
        if isinstance(resultado, str) or resultado is None:
            
            # Se crea el nuevo grupo reposo
            grupoReposo_nuevo = GrupoReposoCalls.crear_grupo_reposo(grupo_reposo)

            # Creamos una lista de objetos reposo con los datos recibidos
            reposos = []

            # Se recorren todos los reposos que se enviaron, normalmente seria 1 solo
            for reposo_info in datos_completos['reposos']:
                reposo = ReposoCalls.retornar_obj_reposo(reposo_info)  # Asociaremos este campo más adelante
                fecha_inicio_reposo = datetime.strptime(reposo_info['fecha_inicio'], "%Y-%m-%d")
                fecha_fin_reposo = datetime.strptime(reposo_info['fecha_fin'], "%Y-%m-%d")
                if fecha_inicio_reposo > fecha_fin_reposo:
                    return "07|La fecha de inicio es mayor a la fin"
                reposos.append(reposo)
            
            # Se pregunta si existre grupo de reporte nuevo y si la lista de reposos tiene algo
            if grupoReposo_nuevo and len(reposos) > 0:

                # Se recorren y se crean
                for i, reposo in enumerate(reposos):
                    reposo.grupo_reposo_id = grupoReposo_nuevo.id
                    ReposoCalls.crear_reposo(reposo)
                return "00|Reposo creado"
            
            return None
        
        # Parte por hacer
        elif resultado[0]:
            grupo_reposo_encontrado = resultado[0]
            reposos_asociados = resultado[1]

            total_dias_reposos = 0  # Inicializamos la variable para almacenar el total de días

            for reposo in reposos_asociados:

                # Calculamos la duración del reposo en días
                duracion_reposo = (reposo.fecha_fin - reposo.fecha_inicio).days + 1
                total_dias_reposos += duracion_reposo  # Sumamos los días al total

            reposos = []

            total_dias_completos = 0  # Inicializamos el total de días de los rangos en datos_completos

            # Se recorren los reposos que se enviaron al servicio
            for reposo_info in datos_completos['reposos']:
                fecha_inicio_reposo = datetime.strptime(reposo_info['fecha_inicio'], "%Y-%m-%d")
                fecha_fin_reposo = datetime.strptime(reposo_info['fecha_fin'], "%Y-%m-%d")
                if fecha_inicio_reposo > fecha_fin_reposo:
                    return "07|La fecha de inicio es mayor a la fin"
                duracion_reposo_completo = (fecha_fin_reposo - fecha_inicio_reposo).days + 1

                # Se recorren los reposos que se consultaron de la base de datos para las validaciones
                for reposo_existente in reposos_asociados:
                    if (fecha_inicio_reposo <= reposo_existente.fecha_fin and fecha_fin_reposo >= reposo_existente.fecha_inicio):
                        return "05|Fecha de reposo se superpone con reposo existente"
                    elif (fecha_inicio_reposo >= reposo_existente.fecha_inicio and fecha_inicio_reposo <= reposo_existente.fecha_fin) or \
                        (fecha_fin_reposo >= reposo_existente.fecha_inicio and fecha_fin_reposo <= reposo_existente.fecha_fin):
                        return "06|Existen 2 o más reposos asociados dentro del rango de fechas"

                total_dias_completos += duracion_reposo_completo

                # Se agregan a una lista los reposos nuevos para ser creados mas adelante
                reposo = ReposoCalls.retornar_obj_reposo(reposo_info)
                reposos.append(reposo)

            total_dias_totales = total_dias_reposos + total_dias_completos

            diasMaximos = 63

            tipoReposo = TipoReposoCalls.get_tipoReposo_id(grupo_reposo_encontrado.tipo_reposo_id)

            if tipoReposo is not None:
                diasMaximos = tipoReposo.maximo_dias

            if total_dias_totales > diasMaximos:
                return "04|La suma de días de reposos es mayor a 63"
            else:
                # Se recorren y se crean
                for i, reposo in enumerate(reposos):
                    reposo.grupo_reposo_id = grupo_reposo_encontrado.id
                    ReposoCalls.crear_reposo(reposo)
                return "00|Reposo creado"
        else:
            return "03|No se encontró ningún Grupo de Reposo para el paciente"

    def sumar_dias_reposos_ultimo_grupo(cedula):
        # Obtener el último grupo de reposos del paciente por su cédula
        grupo_reposos = GrupoReposoCalls.get_grupoReposo_paciente(cedula)

        if grupo_reposos:
            # Obtener el último grupo de reposos (el primero en la lista ordenada)
            ultimo_grupo = grupo_reposos[0]

            # Obtener los reposos asociados al último grupo
            reposos_asociados = ultimo_grupo.reposos

            # Inicializar la variable para almacenar el total de días
            total_dias_reposos = 0

            # Sumar los días de cada reposo
            for reposo in reposos_asociados:
                duracion_reposo = (reposo.fecha_fin - reposo.fecha_inicio).days + 1
                total_dias_reposos += duracion_reposo

            return total_dias_reposos
        else:
            # No se encontraron grupos de reposos para el paciente
            return 0

    def create_pdf_pacientes(pacientes, logo_path, titulo,tipo):
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
 
        if tipo == "pacientes":
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(30, 10, 'Cedula', 1, 0,'C')
            pdf.cell(30, 10, 'Nombre', 1, 0,'C')
            pdf.cell(30, 10, 'Apellido', 1, 0,'C')
            pdf.cell(35, 10, 'Telefono', 1, 0,'C')
            pdf.cell(35, 10, 'Correo', 1, 0,'C')
            pdf.cell(30, 10, 'Días Reposo', 1, 0,'C')  # Agrega este campo solo para pacientes
            pdf.ln()
            # Configurar fuente y tamaño para los datos de los pacientes
            pdf.set_font('Arial', '', 10)

            # Agregar datos de pacientes al PDF
            for paciente in pacientes:
                pdf.cell(30, 10, str(paciente["cedula"]), 1, 0,'C')
                pdf.cell(30, 10, paciente["nombre"], 1, 0,'C')
                pdf.cell(30, 10, paciente["apellido"], 1, 0,'C')
                pdf.cell(35, 10, paciente["telefono"], 1, 0,'C')
                pdf.cell(35, 10, paciente["correo"], 1, 0,'C')
                pdf.cell(30, 10, str(paciente["dias_reposo"]), 1, 0,'C')
                pdf.ln()
        elif tipo == "pacienteIndividual":
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(30, 10, 'Cedula', 1, 0,'C')
            pdf.cell(30, 10, 'Nombre', 1, 0,'C')
            pdf.cell(30, 10, 'Apellido', 1, 0,'C')
            pdf.cell(35, 10, 'Telefono', 1, 0,'C')
            pdf.cell(35, 10, 'Correo', 1, 0,'C')
            pdf.cell(30, 10, 'Días Reposo', 1, 0,'C')  # Agrega este campo solo para pacientes
            pdf.ln()

            pdf.set_font('Arial', '', 10)
            pdf.cell(30, 10, str(pacientes["cedula"]), 1, 0,'C')
            pdf.cell(30, 10, pacientes["nombre"], 1, 0,'C')
            pdf.cell(30, 10, pacientes["apellido"], 1, 0,'C')
            pdf.cell(35, 10, pacientes["telefono"], 1, 0,'C')
            pdf.cell(35, 10, pacientes["correo"], 1, 0,'C')
            pdf.cell(30, 10, str(pacientes["dias_reposo"]), 1, 0,'C')
            pdf.ln()

            pdf.set_font('Arial', 'B', 16)
            pdf.set_text_color(41, 0 ,199)
            pdf.cell(w=190.0, h=40.0, align='C', txt="Reposos", border=0)
            pdf.set_text_color(0.0, 0.0 ,0.0)
            # Agregar cabeceras de columnas
            pdf.set_xy(10.0,100.0)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(40, 10, 'Codigo Asistencial', 1, 0,'C')
            pdf.cell(40, 10, 'Codigo Registro', 1, 0,'C')
            pdf.cell(35, 10, 'Fecha Inicio', 1, 0,'C')
            pdf.cell(35, 10, 'Fecha Fin', 1, 0,'C')
            pdf.cell(35, 10, 'Quien Valida', 1, 0,'C')
            pdf.ln()

            # Agregar datos de pacientes al PDF
            for reposos in pacientes["reposos"]:
                pdf.set_font('Arial', '', 10)
                pdf.cell(40, 10, str(reposos["codigo_asistencial"]), 1, 0,'C')
                pdf.cell(40, 10, reposos["codigo_registro"], 1, 0,'C')
                pdf.cell(35, 10, reposos["fecha_inicio"].split("T")[0], 1, 0,'C')
                pdf.cell(35, 10, reposos["fecha_fin"].split("T")[0], 1, 0,'C')
                pdf.cell(35, 10, reposos["quien_valida"], 1, 0,'C')
                pdf.ln()

        # Llamar al método footer para generar el pie de página
        pdf.footer()

        # Crear un archivo temporal para guardar el PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            pdf_path = temp_file.name
            pdf.output(pdf_path)
        return pdf_path
    