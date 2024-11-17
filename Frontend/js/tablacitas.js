document.addEventListener('DOMContentLoaded', async function() {
    InicializarFechasFacturas()
    await consultarCitas(true)
});

function InicializarFechasFacturas(){
    let fecha = new Date(); //Fecha actual
    fecha.setDate(fecha.getDate()-15);
    let mes = fecha.getMonth()+1; //obteniendo mes
    let dia = fecha.getDate(); //obteniendo dia
    let ano = fecha.getFullYear(); //obteniendo año
    if(dia<10)
        dia='0'+dia; //agrega cero si el menor de 10
    if(mes<10)
        mes='0'+mes //agrega cero si el menor de 10
    document.getElementById('fechaInicio').value=ano+"-"+mes+"-"+dia;

    fecha.setDate(fecha.getDate()+30);
    mes = fecha.getMonth()+1; //obteniendo mes
    dia = fecha.getDate(); //obteniendo dia
    ano = fecha.getFullYear(); //obteniendo año
    if(dia<10)
        dia='0'+dia; //agrega cero si el menor de 10
    if(mes<10)
        mes='0'+mes //agrega cero si el menor de 10
    document.getElementById('fechaFin').value=ano+"-"+mes+"-"+dia;
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

        consultarCitas(false)

    }catch(e){
        mostrarNotificacion("Error: " + e,"#FF0000")  
        console.error('Error:', e);
    }
}

async function consultarCitas(mensaje){
    try {
        const fechaInicio = document.getElementById('fechaInicio')
        const fechaFin = document.getElementById('fechaFin')


        const objeto = {
            fechaInicio: fechaInicio.value,
            fechaFin: fechaFin.value
        }

        const datos = await consultar('cita/ObtenerCitasPorRangoFechas', 'POST', objeto); 

        if(typeof datos === 'undefined' || datos === null || datos.length === 0){
            mostrarNotificacion("No se pudo cambiar el estado a la cita","#FF0000") 
            return
        }

        if(mensaje){
            mostrarNotificacion("Se cambio el estado de la cita","linear-gradient(to right, #00b09b, #96c93d)"); 
        }

        initDataTable(datos.sort((a, b) => new Date(b.fecha.fecha) - new Date(a.fecha.fecha)))

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
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] }
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
                        <button class="btn btn-sm btn-primary" onclick="cambiarEstado(${dato.id},2)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
                                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/>
                            </svg>
                        </button>
                        <button class="btn btn-sm btn-secondary mx-2" onclick="cambiarEstado(${dato.id},3)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                            </svg>
                        </button>
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

