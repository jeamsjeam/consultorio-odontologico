
async function consultarCitas(){
    try {
        const fechaInicio = document.getElementById('fechaInicio')
        const fechaFin = document.getElementById('fechaFin')


        const objeto = {
            fechaInicio: fechaInicio.value,
            fechaFin: fechaFin.value
        }

        const datos = await consultar('cita/ObtenerCitasPorRangoFechas', 'POST', objeto); 

        if(typeof datos === 'undefined' || datos === null || datos.length === 0){
            mostrarNotificacion("No se encontro cita","#FF0000") 
            return
        }
        mostrarNotificacion("Citas encontradas","linear-gradient(to right, #00b09b, #96c93d)"); 

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
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] }
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
                    <td>${dato.fecha.fecha}</td>
                    <td>${dato.servicio.nombre}</td>
                    <td>${dato.estado_cita.nombre}</td>
                    <!-- <td><i class="fa-solid fa-check" style="color: green;"></i></td> -->
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="ModalPersonas(${dato.id},true,'actualizar')"
                        ><i class="bi bi-pen"></i></button>
                        <button class="btn btn-sm btn-danger" onclick="ModalPersonas(${dato.id},true,'eliminar')"
                        ><i class="bi bi-trash3"></i></button>
                         <button class="btn btn-sm btn-info" onclick="generarConstancia(${dato.id})">
                            <i class="bi bi-file-earmark-text"></i>
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

