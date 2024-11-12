document.addEventListener('DOMContentLoaded', async function() {
    await CrearModalePersona()
    await buscarPersona()
    await ObtenerSelect('servicio','servicios-select','Error al cargar los servicios')
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
                                    <div class="col-12">
                                        <div class="mb-3">
                                            <label class="mb-2 text-muted" for="direccion">Direccion</label>
                                            <input id="direccion" type="text" class="form-control" name="direccion" value="" required>
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
    const datosUsuario = JSON.parse(sessionStorage.getItem('usuario'));

    const datos = await consultar('persona/ObtenerPorUsuario/' + datosUsuario.id, 'GET', null); 

    localStorage.removeItem('persona');
    localStorage.setItem('persona', JSON.stringify(datos))

    if(typeof datos === 'undefined' || datos === null){
        controlarModalPersona(true)
    }
    return
}

async function registrarPersona(){
    try {
        let datosUsuario = JSON.parse(sessionStorage.getItem('usuario'));
    
        let cedula = document.getElementById('cedula')
        let nombre = document.getElementById('nombre')
        let apellido = document.getElementById('apellido')
        let telefono = document.getElementById('telefono')
        let direccion = document.getElementById('direccion')
        let municipio = document.querySelector('select[name="municipio"]')
    
        const objeto = {
            cedula: cedula.value,
            nombre: nombre.value,
            apellido: apellido.value,
            telefono: telefono.value,
            direccion: direccion.value,
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
    
        return
    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}
