document.addEventListener('DOMContentLoaded', async function() {

    await CrearModalePersona()
    await buscarPersona()
    await ObtenerSelect('servicio','servicios-select','Error al cargar los servicios')

    await populateMonthAndYear();
    
});

// Variables globales
var modalPersona = null;

async function CrearModalePersona() {
    const modalDiv = document.createElement('div');
    modalDiv.innerHTML = `
        <div class="modal fade" id="modalPersona" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="modalPersonaLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <form action="#" method="POST" onsubmit="event.preventDefault();"></form>
                            <div class="modal-header">
                                <h5 class="modal-title" id="modalPersonaLabel">Registrar Persona</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" onclick="window.location.href = 'index.html';"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="cedula">Cedula</label>
                                            <input id="cedula" type="text" class="form-control" name="cedula" value="" required autofocus>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="telefono">Telefono</label>
                                            <input id="telefono" type="text" class="form-control" name="telefono" value="" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="nombre">Nombre</label>
                                            <input id="nombre" type="text" class="form-control" name="nombre" value="" required>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="apellido">Apellido</label>
                                            <input id="apellido" type="text" class="form-control" name="apellido" value="" required>
                                        </div>
                                    </div>
                                </div> 
                                <div class="row">
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="direccion">Direccion</label>
                                            <input id="direccion" type="text" class="form-control" name="direccion" value="" required>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="fechaNacimiento">Fecha Nacimiento</label>
                                            <input id="fechaNacimiento" type="date" class="form-control" name="fechaNacimiento" value="" required>
                                        </div>
                                    </div>
                                </div> 
                                <div class="row">
                                    <div class="col-4">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="pais">Pais</label>
                                            <select name="pais" class="form-select" aria-label="Default select example" id="paises-select">
                                                <!-- Agrega opciones del select si es necesario -->
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="estado">Estado</label>
                                            <select name="estado" class="form-select" aria-label="Default select example" id="estados-select">
                                                <!-- Agrega opciones del select si es necesario -->
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="municipio">Municipio</label>
                                            <select name="municipio" class="form-select" aria-label="Default select example" id="municipios-select">
                                                <!-- Agrega opciones del select si es necesario -->
                                            </select>
                                        </div>
                                    </div>
                                </div>   
                            </div>
                            <div class="modal-footer">
                                <button type="submit" class="btn btn-primary ms-auto" onclick="registrarPersona()">Registrar</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>`;
    document.body.appendChild(modalDiv);
    modalPersona = new bootstrap.Modal(document.getElementById('modalPersona'));
    await ObtenerSelect('pais','paises-select','Error al cargar los paises')
    await ObtenerSelect('estado','estados-select','Error al cargar los estados')
    await ObtenerSelect('municipio','municipios-select','Error al cargar los municipios')
}

// Funcion que abre o cierra el modal del loading
function controlarModalPersona(bandera){
    return new Promise((resolve) => {
        const elementoModal = document.getElementById('modalPersona');
        elementoModal.addEventListener(bandera ? 'shown.bs.modal' : 'hidden.bs.modal', () => {
            resolve();
        }, { once: true });
        if(bandera)
            modalPersona.show();
        else
            modalPersona.hide();
    });
}

async function buscarPersona(){
    try {
        const datosUsuario = JSON.parse(sessionStorage.getItem('usuario'));

        const datos = await consultar('persona/ObtenerPorUsuario/' + datosUsuario.id, 'GET', null); 

        
        if(typeof datos === 'undefined' || datos === null){
            controlarModalPersona(true)
            return
        }

        localStorage.removeItem('persona');
        localStorage.setItem('persona', JSON.stringify(datos))
        await DatosTabla()

        return
    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

async function registrarPersona(){
    try {
        let datosUsuario = JSON.parse(sessionStorage.getItem('usuario'));
    
        let cedula = document.getElementById('cedula')
        let nombre = document.getElementById('nombre')
        let apellido = document.getElementById('apellido')
        let telefono = document.getElementById('telefono')
        let direccion = document.getElementById('direccion')
        let fechaNacimiento = document.getElementById('fechaNacimiento')
        let municipio = document.querySelector('select[name="municipio"]')
    
        const objeto = {
            cedula: cedula.value,
            nombre: nombre.value,
            apellido: apellido.value,
            telefono: telefono.value,
            direccion: direccion.value,
            fechaNacimiento: fechaNacimiento.value,
            municipioId: parseInt(municipio.selectedOptions[0].value),
            tipoPersonaId: 2,
            usuarioId: datosUsuario.id
        }
 
        const datos = await consultar('persona/CrearPersona', 'POST', objeto); 

        if(typeof datos === 'undefined' || datos === null){
            mostrarNotificacion("No se pudo registrar persona","#FF0000") 
            return
        }
        localStorage.removeItem('persona');
        localStorage.setItem('persona', JSON.stringify(datos))
    
        cedula.value = ""
        nombre.value = ""
        apellido.value = ""
        telefono.value = ""
        direccion.value = ""
        fechaNacimiento.value = ""
        municipio.value = 1
    
        controlarModalPersona(false)

        mostrarNotificacion("Persona registrada ","linear-gradient(to right, #00b09b, #96c93d)"); 
    
        return
    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

async function crearCita(){
    try {

        let datosPersona = JSON.parse(localStorage.getItem('persona'));
    
        let fecha = document.getElementById('fecha')
        let servicioId = document.querySelector('select[name="servicio"]')

        const objeto = {
            cedula: datosPersona.cedula,
            fecha: fecha.value,
            servicioId: parseInt(servicioId.selectedOptions[0].value)
        }

        const datos = await consultar('cita/CrearCita', 'POST', objeto); 

        if(typeof datos === 'undefined' || datos === null){
            mostrarNotificacion("No se pudo crear cita","#FF0000") 
            return
        }

        fecha.value = ""
        servicioId.value = 1

        mostrarNotificacion("Cita creada ","linear-gradient(to right, #00b09b, #96c93d)"); 
        document.getElementById('fecha').value = ''
        await renderCalendar();
        await DatosTabla()
    
        return
    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

async function DatosTabla(){
    try{

        let datosPersona = JSON.parse(localStorage.getItem('persona'));

        let data = await consultar("cita/ObtenerPorCedulaMenosBorradas/" + datosPersona.cedula, 'GET', null);
        if(typeof data === 'undefined' || data === null || data.length === 0){
            mostrarNotificacion("No se encontro ningun " + error,"#FF0000") 
        }

        initDataTable(data.sort((a, b) => new Date(b.fecha.fecha) - new Date(a.fecha.fecha)))
        
	}catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

var dataTable;
var dataTableIsInitialized = false;
var numeroPorPagona = 10;

const dataTableOptions = {
    scrollY: 'auto',  // Ajusta la altura automáticamente
    scrollCollapse: true,  // Permite colapsar la tabla si hay menos registros
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8] }
    ],
    pageLength: numeroPorPagona,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ningún registro encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún registro encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

function initDataTable(datos) { 
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    listaDatos(datos);

    dataTable = $("#datatable_citas").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
}

function listaDatos(datos) {
    try {

        let content = ``;
        datos.forEach((dato, index) => {
            content += `
                 <tr>
                    <td>${index + 1}</td>
                    <td>${dato.persona.cedula}</td>
                    <td>${dato.persona.nombre}</td>
                    <td>${dato.persona.apellido}</td>
                    <td>${dato.persona.fechaNacimiento}</td>
                    <td>${dato.persona.telefono}</td>
                    <td>${dato.fecha.fecha}</td>
                    <td>${dato.servicio.nombre}</td>
                    <td>${dato.estado_cita.nombre}</td>
                    <!-- <td><i class="fa-solid fa-check" style="color: green;"></i></td> -->
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="cambiarEstado(${dato.id},4)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
                            </svg>
                        </button>
                    </td>
                </tr>`;
        });
        tableBody_citas.innerHTML = content;
    } catch (e) {
        mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
    }
}

async function cambiarEstado(id, estado){
    try {
        const objeto = {
            id: id,
            estadoCitaId: estado
        }

        const datos = await consultar('cita/ActualizarCita', 'POST', objeto); 

        if(typeof datos === 'undefined' || datos === null){
            mostrarNotificacion("No se pudo cambiar el estado de la cita","#FF0000") 
            return
        }
        mostrarNotificacion("Se cambio el estado de la cita","linear-gradient(to right, #00b09b, #96c93d)"); 

        await renderCalendar();
        await DatosTabla()

    }catch(e){
        mostrarNotificacion("Error: " + e,"#FF0000")  
        console.error('Error:', e);
    }
}

// Selecciona los elementos HTML para los selectores de mes, año y el contenedor del calendario
const monthSelect = document.getElementById("month");
const yearSelect = document.getElementById("year");
const calendar = document.getElementById("calendar");

// Función para poblar los selectores de mes y año en el HTML
async function populateMonthAndYear() {
    // Llena el selector de mes con los nombres de los meses
    for (let m = 0; m < 12; m++) {
        const option = document.createElement("option");
        option.value = m;
        option.text = new Date(0, m).toLocaleString("es", { month: "long" }); // Nombre del mes en español
        monthSelect.appendChild(option);
    }

    // Define el año actual y crea una lista de años desde el actual - 5 hasta el actual + 5
    const currentYear = new Date().getFullYear();
    for (let y = currentYear; y <= currentYear + 2; y++) {
        const option = document.createElement("option");
        option.value = y;
        option.text = y;
        yearSelect.appendChild(option);
    }

    // Selecciona el mes y año actuales por defecto en los selectores
    monthSelect.value = new Date().getMonth();
    yearSelect.value = currentYear;

    await renderCalendar();
}

var mes = 1
var anio = 2024

// Función para renderizar el calendario según el mes y año seleccionados
async function renderCalendar() {

    document.getElementById('fecha').value = ''

    // Obtiene el mes y año seleccionados
    const month = parseInt(monthSelect.value);
    const year = parseInt(yearSelect.value);

    // Calcula el primer día de la semana y el total de días del mes seleccionado
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Calcula el total de días del mes anterior
    const previousMonthDays = new Date(year, month, 0).getDate();

    // Limpia el contenido actual del calendario
    calendar.innerHTML = "";

    // Definición de los nombres de los días de la semana
    const daysOfWeek = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];

    anio = year
    mes = new Date(year, month + 2, 0).getMonth()
    const diaActual = new Date().getDate()
    const mesActual = new Date().getMonth()
    const anioActual = new Date().getFullYear()

    let datosDiasNoDisponibles = []
    if((month >= mesActual && year === anioActual) || (year > anioActual)){
        datosDiasNoDisponibles = await diasSinCitas(1, daysInMonth, (mes === 0 ? 12 : (mes < 10 ? '0' + mes : mes)), anio)
    }

    const datosCitasPersona = await citasPersona(1, daysInMonth, (mes === 0 ? 12 : (mes < 10 ? '0' + mes : mes)), anio)

    // Agrega encabezados de los días de la semana al calendario
    daysOfWeek.forEach(day => {
        const dayElement = document.createElement("div");
        dayElement.textContent = day;
        dayElement.classList.add("header");
        calendar.appendChild(dayElement);
    });
    
    // Agrega celdas inactivas al calendario para los días del mes anterior
    for (let i = firstDay - 1; i >= 0; i--) {
        const inactiveCell = document.createElement("div");
        inactiveCell.textContent = previousMonthDays - i;
        inactiveCell.classList.add("inactive");
        calendar.appendChild(inactiveCell);
    }

    // Agrega los días del mes actual al calendario
    for (let day = 1; day <= daysInMonth; day++) {

        const dayCell = document.createElement("div");

        dayCell.textContent = day;

        if(datosCitasPersona.findIndex(x => x === day) !== -1){
            dayCell.classList = "blue";
        }else{

            if(month < mesActual && year <= anioActual){
                dayCell.classList.add("inactive");
            }else{
                if(day < diaActual && month === mesActual && year === anioActual){
                    dayCell.classList.add("inactive");
                }else if(datosDiasNoDisponibles.findIndex(x => x === day) !== -1){
                    dayCell.classList.add("gray");
                }else{
                    dayCell.classList.add("white"); // Establece el color inicial en blanco
                    dayCell.onclick = () => changeColor(dayCell); // Llama a la función changeColor cuando se hace clic en el día
                }
            }
        }

        calendar.appendChild(dayCell);
    }
    
    // Agrega celdas inactivas para llenar la última fila con días del mes siguiente
    const totalCells = firstDay + daysInMonth;
    const remainingCells = 7 - (totalCells % 7);
    if (remainingCells < 7) {
        for (let j = 1; j <= remainingCells; j++) {
            const inactiveCell = document.createElement("div");
            inactiveCell.textContent = j;
            inactiveCell.classList.add("inactive");
            calendar.appendChild(inactiveCell);
        }
    }
}

var dayCellAnterior = null

// Función para cambiar el color de un día del calendario
function changeColor(dayCell) {
    console.log(dayCell)
    if(typeof dayCellAnterior !== 'undefined' && dayCellAnterior !== null && dayCell.className !== 'green'){
        dayCellAnterior.className = "white";
    }

    if(dayCell.className === 'green'){
        dayCell.className = 'white'
        document.getElementById('fecha').value = ''
    }else{
        dayCell.className = 'green'
        day = dayCell.innerHTML
        if(dayCell.innerHTML < 10){
            day = '0'+ dayCell.innerHTML
        }
        document.getElementById('fecha').value = anio +'-' + (mes === 0 ? 12 : (mes < 10 ? '0' + mes : mes)) + '-' + day
    }

    dayCellAnterior = dayCell    
}

async function diasSinCitas(firstDay, daysInMonth, month, year){
    try {
        const objeto = {
            fechaInicio: year + '-' + month + '-0' + firstDay,
            fechaFin: year + '-' + month + '-' + daysInMonth
        }

        const datos = await consultar('cita/CalendarioNoDisponible', 'POST', objeto); 
      
        if(typeof datos === 'undefined' || datos === null){
            controlarModalPersona(true)
            return
        }

        return datos
    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

async function citasPersona(firstDay, daysInMonth, month, year){
    try {
        let datosPersona = JSON.parse(localStorage.getItem('persona'));

        const objeto = {
            cedula: datosPersona.cedula,
            fechaInicio: year + '-' + month + '-0' + firstDay,
            fechaFin: year + '-' + month + '-' + daysInMonth
        }

        const datos = await consultar('cita/ObtenerCitasPersonaPorRangoFechas', 'POST', objeto); 
      
        if(typeof datos === 'undefined' || datos === null){
            controlarModalPersona(true)
            return
        }

        return datos
    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}
